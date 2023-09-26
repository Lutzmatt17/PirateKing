import socket
import threading
from threading import Lock
from game import Game
from deck import Deck
import time
import json
import logging
from datetime import datetime
from queue import Queue
import uuid

logging.basicConfig(level=logging.DEBUG)

class WaitingRoom:
    def __init__(self, server, room_name):
        self.min_players = 3
        self.max_players = 8
        # List of player objects containing all relevant info about each player
        self.players = []
        self.players_lock = Lock()
        self.timer_duration = 90
        self.game_started = False
        self.room_name = room_name
        self.server = server
        self.room_id = self.server.generate_unique_id()
    
    def get_min_players(self):
        return self.min_players
    
    def get_max_players(self):
        return self.max_players
    
    def get_player_num(self):
        return len(self.players)

    def get_room_name(self):
        return self.room_name

    def has_game_started(self):
        return self.game_started
    
    def set_game_started(self, game_started):
        self.game_started = game_started

    def is_available(self):
        room_available = False
        if self.get_player_num() < self.get_max_players():
            room_available = True
        return room_available

    # Adds a player if the room is available, in thread safe fashion. 
    # Returns True if the player was added, false if not.
    def add_player(self, player):
        with self.players_lock:
            room_available = self.is_available()
            if room_available:
                self.players.append(player)
                return room_available
            return room_available

    def broadcast_timer(self, timer):
         with self.players_lock:
            for player in self.players:
                player_socket = player.get('player_socket')
                try:
                    self.server.send_with_length(player_socket, timer)
                except socket.error as e:
                    print(str(e))

    def broadcast(self, message):
        with self.players_lock:
            for player in self.players:
                player_socket = player.get('player_socket')
                try:
                    self.server.send_with_length(player_socket, message)
                    ack = self.server.receive_with_length(player_socket)
                    with self.server.ack_lock:
                        self.server.ack_queue.put(ack)
                    print(ack)
                except socket.error as e:
                    print(str(e))

    def start_timer(self, t):
        while t >= 0:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            serialized_timer = self.server.make_message('countdown', timer)
            self.broadcast_timer(serialized_timer)
            time.sleep(1)
            t -= 1
        self.start_game()

    def start_game(self):
        logging.info(f"Game starting with players...\n")
        with self.players_lock:
            for player in self.players:
                player_socket = player.get('player_socket')
                try:
                    print(player_socket.getpeername())
                except socket.error as e:
                    logging.error(f"Socket error, possibly bad file descripter: {e}")
                    player_socket.close()

        # Notify the server to start the game with the players
        self.server.start_game(self, self.players)


# Creating a server

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server address and port number
        self.server_address = ("172.28.5.101", 5555)
        # list of all clients connected to the server
        self.clients = []
        # Lock for accessing shared list of clients
        self.client_lock = Lock()
        # maps each client to game id to keep track of which game they're in
        self.client_game_map = {}
        # lock for the client to game mapping dict
        self.client_game_map_lock = Lock()
        # maps each game id to it's respective, active game
        self.active_games = {}
        # Lock for game instances
        self.active_games_lock = Lock()
        # Dict that holds command queues for each game
        self.game_commands = {}
        # Lock for game_commands dict
        self.game_commands_lock = Lock()
        # List of waiting rooms
        self.waiting_rooms = []
        # Room lock to keep accessing of waiting rooms by multiple clients thread safe
        self.room_lock = Lock()
        # Acknowledgement Queue
        self.ack_queue = Queue()
        # Acknowledgement Lock
        self.ack_lock = Lock()
        # Object that sets the current game state for each game based on the game_id
        self.game_states = {}
        # Lock for game_states object
        self.game_states_lock = Lock()
        # tring to bind the socket to the server and throw error if it doesn't bind
        try:
            self.server_socket.bind(self.server_address)
            logging.info(f"Server started at {self.server_address}")

        except socket.error as e:
            logging.error(f"Socket error: {str(e)}")
        # listen for client connections from players    
        self.server_socket.listen(2)
        print("Waiting for players to join...")

    def threaded_client(self, client_socket, player):
        # client_socket.settimeout(5)  # Set timeout to 5 seconds
        client_state = "INIT"
        try:
            while True:
                if client_state == "INIT":
                    # logging.info(f"Receiving username...")
                    player = self.decode_message(self.receive_with_length(client_socket))
                    player['player_socket'] = client_socket
                    username = player.get('username')
                    logging.info(f"Received username...")
                    find_room = self.make_message('message', "Finding a room for you...")
                    # logging.info(f"Sending message...")
                    self.send_with_length(client_socket, find_room)
                    logging.debug(f"Sent message to {client_socket.getpeername()}")

                    ack = self.receive_with_length(client_socket)
                    with self.ack_lock:
                        self.ack_queue.put(ack)
                    logging.debug(f"Received acknowledgement: {ack}")

                    room = self.find_available_room(player)
                    logging.info(f"Room found for player {player}")
                    room.broadcast(self.make_message('message', username + " is connected to: " + room.get_room_name()))
                    if room.has_game_started():
                        client_state = "GAMEPLAY"
                    else:
                        client_state = "WAITING"
                elif client_state == "GAMEPLAY":
                    # Fetch the game_id
                    with self.client_game_map_lock:
                        game_id = self.client_game_map.get(client_socket)  

                    if game_id is None:
                        client_socket.close()
                        return
                    gameplay_state = ''
                    while gameplay_state != "GAMEOVER":
                        with self.game_states_lock:
                            gameplay_state = self.game_states.get(game_id)
                        if gameplay_state == "DEALING":
                            logging.info(f"In DEALING phase...")
                            continue # Let game thread handle dealing
                        elif gameplay_state == "BIDDING":
                            logging.info(f"In BIDDING phase...")
                            bid_command = self.decode_message(self.receive_with_length(client_socket))
                            logging.info(f"This is what bid command is receiving...{bid_command}")
                            with self.game_commands_lock:
                                self.game_commands.get(game_id).put(bid_command)
                elif client_state == "WAITING":
                    logging.info(f"Waiting for game to start...")
                    if room.has_game_started():
                        client_state = "GAMEPLAY"
                    continue # Keep looping until the game starts
             
        except Exception as e:
            logging.error(f"Exception in threaded_client for player {username}: {str(e)}")
        finally:
            print(f"Lost connection for player {player}")
            client_socket.close()

    def find_available_room(self, player):
        with self.room_lock:
            unavailable_count = 0
            for room in self.waiting_rooms:
                if room.add_player(player):
                    return room
                else:
                    unavailable_count += 1
            if unavailable_count == len(self.waiting_rooms):
                new_room = self.make_new_room()
                logging.info(f"New room created: {new_room.get_room_name()}")
                new_room.add_player(player)
                self.waiting_rooms.append(new_room)
                return new_room
        
    def make_new_room(self):
        new_room_name = "room" + str(len(self.waiting_rooms) + 1) 
        return WaitingRoom(self, new_room_name)
    
    # Makes a ready to send, serialized json message
    def make_message(self, type, content):
        return json.dumps({'type': type, 'content': content})

    def decode_message(self, message):
        return json.loads(message)

    def send_with_length(self, client_socket, message):
        message_length = str(len(message))
        # Pad with zeros to make it a 4-byte length prefix
        message_length = message_length.zfill(4)
        # Concatenate the length prefix and the actual message
        full_message = message_length + message
        try:
            client_socket.send(full_message.encode())
        except BrokenPipeError as e:
            logging.error(f"Client disconnected because: {str(e)}")
            client_socket.close()
        except socket.error as e:
            logging.error(f"Socket error, possibly bad file descriptor")
            client_socket.close()

    def receive_with_length(self, client_socket):
        message_length = int(client_socket.recv(4).decode())
        # print(message_length)
        message = client_socket.recv(message_length).decode()
        return message

    def deal_players(self, game):
        """
        Deal hands to all players in the game.
        """
        i = 0
        for player in game.get_players():
                # logging.info(f"These are the players: {game.get_players()} in room: {game.get_room()}")
                player_socket = player.get('player_socket')
                hand = game.deal_hand()
                player['hand'] = hand
                logging.info(f"Hand has been made... for player: {i}")
                serialized_hand = self.make_message('gameplay_data', hand)
                self.send_with_length(player_socket, serialized_hand)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                logging.info(f"Sent hand: {hand} to player: {i} at: {current_time}")
                # Get the current timestamp and print it
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                # print(f"Waiting for ack at: {current_time} from player {i}")
                # ack = self.receive_with_length(player)
                # with self.ack_lock:
                #     self.ack_queue.put(ack)
                # ack = player.recv(2048).decode()
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                # logging.debug(f"Received acknowledgement: {ack} at: {current_time}")
                i += 1

    def accept_connections(self):
        current_player = 0
        while True:
            client_socket, addr = self.server_socket.accept()
            logging.info(f"New client connected from {addr}")
            client_thread = threading.Thread(target=self.threaded_client, args=(client_socket, current_player))
            logging.info(f"Thread started for client {current_player}")
            client_thread.start()
            current_player += 1


    def monitor_rooms(self):
        while True:
            for room in self.waiting_rooms:
                if room.get_player_num() >= room.get_min_players() and not room.has_game_started():
                    logging.info(f"Timer started...")
                    room.start_timer(10)
            time.sleep(1)

    def process_acks(self):
        while True:
            ack = self.ack_queue.get()  # Dequeue an acknowledgment
            if ack:  # Perform your acknowledgment logic here
                logging.debug(f"Acknowledgement received: {ack}")

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def handle_client_command(self, game_instance, command):
        command_type = command.get('type')
        player_id = command.get('player_id')

        if command_type == 'PLAY_CARD':
            card = command.get('data')
            if game_instance.validate_play_card(player_id, card): 
                game_instance.play_card(player_id, card)
        elif command_type == 'BID':
            bid = command.get('data')
            logging.info(f"This is the bid: {bid} for: {player_id}")
            if game_instance.validate_bid(player_id):
                game_instance.make_bid(player_id, bid)

    def event_timer(self, t):
        while t >= 0:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            serialized_timer = self.server.make_message('countdown', timer)
            self.broadcast_timer(serialized_timer)
            time.sleep(1)
            t -= 1

    def start_game(self, room, players):
        game_id = self.generate_unique_id()
        game = Game(players, room.get_room_name(), game_id)
        with self.active_games_lock:
            self.active_games[game_id] = game
        with self.game_commands_lock:
            self.game_commands[game_id] = Queue()
        with self.game_states_lock:
            self.game_states[game_id] = ''
        for player in players:
            player_socket = player.get('player_socket')
            self.client_game_map[player_socket] = game.get_game_id()
        room.set_game_started(True)
        game_thread = threading.Thread(target=self.run_game, args=(game, room))
        game_thread.start()

    def run_game(self, game, room):
        # implement game logic here
        round = game.get_round()
        while round <= game.get_max_rounds():
            logging.info(f"Starting round {game.get_round()}")
            deck = Deck()
            game.set_deck(deck)
            game.get_deck().shuffle()
            if round > 1:
                game.choose_next_dealer()
                game.who_goes_first()
            logging.info(f"{game.get_dealer().get('username')} is dealing round: {round}!")
            logging.info(f"{game.get_current_player().get('username')} is playing first this round...")
            with self.game_states_lock:
                self.game_states[game.get_game_id()] = 'DEALING'
            self.deal_players(game)
            logging.info(f"Cards have been dealt to all players for round: {round}")
            room.broadcast(self.make_message('message', f"Dealt cards to players in {room.get_room_name()} for round {round}, please make your bids now!"))
            with self.game_states_lock:
                self.game_states[game.get_game_id()] = 'BIDDING'
            time.sleep(60)
            with self.game_commands_lock:
                bid_q = self.game_commands.get(game.get_game_id())
            logging.info(f"Bids have been collected for round: {round}...")
            while not bid_q.empty():
                bid_command = bid_q.get()
                self.handle_client_command(game, bid_command)
            logging.info(f"Bids:{game.get_bids()} have been processed for round: {round}!")
            # with self.game_states_lock:
            #     self.game_states[game.get_game_id()] = 'PLAYING_CARDS'

            # with self.game_commands_lock:
            #     play_q = self.game_commands.get(game.get_game_id())

            # while not play_q.empty():
            #     play_command = play_q.get()
            #     self.handle_client_command(game, play_command)
            logging.info(f"Going to sleep... Goodnight")
            time.sleep(100)    
            round = game.increment_round()

class ServerDriver:
    def __init__(self):
        self.server = Server()
        monitor_thread = threading.Thread(target=self.server.monitor_rooms)
        ack_processing_thread = threading.Thread(target=self.server.process_acks)
        monitor_thread.start()
        ack_processing_thread.start()
    
    def main(self):
        self.server.accept_connections()


if __name__ == "__main__":
    server_driver = ServerDriver()
    server_driver.main()