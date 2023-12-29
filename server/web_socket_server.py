import asyncio
from asyncio import Lock
import uuid
import websockets
import logging
import json
from game import Game

# logging.basicConfig(level=logging.DEBUG)

class WaitingRoom:
    """
    The WaitingRoom class represents a waiting room in the server where players can join before a game starts.
    """
    def __init__(self, server, room_name):
        """
        Initializes a new instance of the WaitingRoom class.
        
        Args:
            server (WebSocketServer): The server that this waiting room belongs to.
            room_name (str): The name of the waiting room.
        """
        self.min_players = 3
        self.max_players = 3
        # List of player objects containing all relevant info about each player
        self.players = []
        self.player_sockets = []
        self.timer_duration = 90
        self.game_started = False
        self.room_name = room_name
        self.server = server
        self.room_id = self.server.generate_unique_id()
    
    def get_min_players(self):
        """
        Returns the minimum number of players required to start a game.
        
        Returns:
            int: The minimum number of players required to start a game.
        """
        return self.min_players
    
    def get_max_players(self):
        """
        Returns the maximum number of players that can join a game.
        
        Returns:
            int: The maximum number of players that can join a game.
        """
        return self.max_players
    
    def get_player_num(self):
        """
        Returns the current number of players in the waiting room.
        
        Returns:
            int: The current number of players in the waiting room.
        """
        return len(self.players)

    def get_room_name(self):
        """
        Returns the name of the waiting room.
        
        Returns:
            str: The name of the waiting room.
        """
        return self.room_name

    def has_game_started(self):
        """
        Returns a boolean indicating whether the game has started or not.
        
        Returns:
            bool: True if the game has started, False otherwise.
        """
        return self.game_started
    
    def set_game_started(self, game_started):
        """
        Sets the game_started flag to the provided value.
        
        Args:
            game_started (bool): The value to set the game_started flag to.
        """
        self.game_started = game_started

    def is_available(self):
        """
        Returns a boolean indicating whether the room is available for new players to join.
        
        Returns:
            bool: True if the room is available for new players to join, False otherwise.
        """
        room_available = False
        if self.get_player_num() < self.get_max_players():
            room_available = True
        return room_available
    
    def add_player(self, player, websocket):
        """
        Adds a player to the waiting room if the room is available. This method is thread safe.
        
        Args:
            player (Player): The player to add to the waiting room.
            websocket (websockets.WebSocketServerProtocol): The websocket of the client to add to the waiting room.
        
        Returns:
            bool: True if the player was added, False otherwise.
        """
        room_available = self.is_available()
        if room_available:
            self.players.append(player)
            self.player_sockets.append(websocket)
        return room_available

    async def broadcast_timer(self, timer):
        """
        Broadcasts the current timer value to all players in the waiting room. This method is thread safe.
        
        Args:
            timer (str): The current timer value to broadcast.
        """
        for websocket in self.player_sockets:
            await websocket.send(timer)

    async def broadcast(self, message):
        """
        Broadcasts a message to all players in the waiting room. This method is thread safe.
        
        Args:
            message (str): The message to broadcast.
        """
        for websocket in self.player_sockets:
            await websocket.send(message)

    async def start_timer(self, t):
        """
        Starts a countdown timer for the specified duration. Once the timer reaches zero, the game starts.
        
        Args:
            t (int): The duration of the timer in seconds.
        """
        while t >= 0:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            serialized_timer = self.server.make_message('countdown', timer)
            await self.broadcast_timer(serialized_timer)
            await asyncio.sleep(1)
            t -= 1
        await self.start_game()

    async def start_game(self):
        """
        Starts the game with the current players in the waiting room.
        """
        logging.info(f"Game starting with players...\n")
        for websocket in self.player_sockets:
            try:
                print(websocket.remote_address)
            except Exception as e:
                logging.error(f"WebSocket error: {e}")
                await websocket.close()

        # Notify the server to start the game with the players
        await self.server.start_game(self, self.players, self.player_sockets)

class ActionTranslator:
    """
    The ActionTranslator class is responsible for translating network commands into game actions and game states into network actions.
    """
    def __init__(self):
        """
        Initializes a new instance of the ActionTranslator class.
        """
        self.accept_commands_flag = asyncio.Event()
        self.send_game_state_flag = asyncio.Event()
        self.advance_game_state_flag = asyncio.Event()
    
    def get_accept_commands_flag(self):
        """
        Returns the flag indicating whether the game is accepting commands.
        
        Returns:
            threading.Event: The flag indicating whether the game is accepting commands.
        """
        return self.accept_commands_flag
    
    def get_send_game_state_flag(self):
        """
        Returns the flag indicating whether the game state should be sent.
        
        Returns:
            threading.Event: The flag indicating whether the game state should be sent.
        """
        return self.send_game_state_flag
    
    def get_advance_game_state_flag(self):
        """
        Returns the flag indicating whether the game state should be advanced.
        
        Returns:
            threading.Event: The flag indicating whether the game state should be advanced.
        """
        return self.advance_game_state_flag

    def network_to_game_action(self, network_command, player_id):
        """
        Translates a network command into a game action.
        
        Args:
            network_command (str): The network command to translate.
            player_id (str): The ID of the player sending the command.
        
        Returns:
            dict: The translated game action.
        """
        command = network_command.split()
        command_type = command[0]

        if command_type == "/play":
            card_index = int(command[1])
            command_type = "PLAY_CARD"
            game_action = {"type": command_type, "player_id": player_id, "card_index": card_index}
        elif command_type =="/bid":
            bid = int(command[1])
            command_type = "BID"
            game_action = {"type": command_type, "player_id": player_id, "bid": bid}
        return game_action
    
    def game_state_to_network(self, game_state):
        """
        Translates a game state into a network action.
        
        Args:
            game_state (GameState): The game state to translate.
        
        Returns:
            dict: The translated network action.
        """

        if game_state.get_phase() == "STARTING":
            network_action = {'round': game_state.get_round(),
                              'tricks': game_state.get_tricks(),
                              'phase': game_state.get_phase()}
        elif game_state.get_phase() == "DEALING":
            network_action = {'dealer': game_state.get_dealer(),
                              'round': game_state.get_round(),
                              'hands': game_state.get_hands(),
                              'phase': game_state.get_phase()}
        elif game_state.get_phase() == "START_BIDDING":
            network_action = {'phase': game_state.get_phase()}
        elif game_state.get_phase() == "BIDDING":
            network_action = {'bids': game_state.get_bids(),
                              'phase': game_state.get_phase()}
        elif game_state.get_phase() == "START_PLAYING":
            network_action = {'phase': game_state.get_phase(),
                              'first_player': game_state.get_current_player()}
        elif game_state.get_phase() == "PLAYING":
            network_action = {'phase': game_state.get_phase(),
                              'previous_player': game_state.get_previous_player(),
                              'current_player': game_state.get_current_player(),
                              'trick': game_state.get_trick(),
                              'player_num': len(game_state.get_players())}
        elif game_state.get_phase() == "RESOLVING":
            network_action = {'trick_winner': game_state.get_trick_winner(),
                              'phase': game_state.get_phase(),
                              'hands': game_state.get_hands()}
        elif game_state.get_phase() == "CALCULATE_SCORES":
            network_action = {'score_sheet': game_state.get_score_sheet(),
                              'phase': game_state.get_phase()}
 
        # self.set_send_game_state_flag(True)

        # self.get_send_game_state_flag().set()
        return network_action

class WebSocketServer:
    def __init__(self):
        # Set to keep track of connected websockets
        self.connected = set()
        # List to keep track of waiting rooms
        self.waiting_rooms = []
        # Lock for thread safety
        self.ack_lock = Lock()
        # Queue for acknowledgements
        self.ack_queue = asyncio.Queue()
        # Lock for game states
        self.game_states_lock = Lock()
        # Dictionary for game states
        self.game_states = {}
        # Lock for game actions
        self.game_actions_lock = Lock()
        # Dictionary for game actions
        self.game_actions = {}
        # Dictionary for client game map
        self.client_game_map = {}
        # Dictionary for action translators
        self.action_translators = {}
        # Lock for action translators
        self.action_translators_lock = Lock()
        # Dictionary for game state acknowledgements
        self.game_state_acks = {}
        # Lock for game state acknowledgements
        self.game_state_acks_lock = Lock()
        # Dictionary for active games
        self.active_games = {}
        # Lock for active games
        self.active_games_lock = Lock()
        # Lock for room safety
        self.room_lock = Lock()

    def generate_unique_id(self):
        """
        Generates a unique ID.

        Returns:
            str: The unique ID.
        """
        return str(uuid.uuid4())

    async def monitor_waiting_rooms(self):
        """
        This function constantly monitors the waiting rooms to see if they're ready to start their game.
        """
        while True:
            for room in self.waiting_rooms:
                if room.get_player_num() >= room.get_min_players() and not room.has_game_started():
                    # room.set_game_started(True)
                    await room.start_timer(10)
            await asyncio.sleep(1)

    async def find_available_room(self, player, client_socket):
        """
        Finds an available room for a player to join. If no room is available, a new room is created.
        
        Args:
            player (dict): The player to add to a room.
            client_socket (socket): The socket of the player.

        Returns:
            WaitingRoom: The room the player was added to.
        """
        async with self.room_lock:
            unavailable_count = 0
            for room in self.waiting_rooms:
                if room.add_player(player, client_socket):
                    return room
                else:
                    unavailable_count += 1
            if unavailable_count == len(self.waiting_rooms):
                new_room = self.make_new_room()
                logging.info(f"New room created: {new_room.get_room_name()}")
                new_room.add_player(player, client_socket)
                self.waiting_rooms.append(new_room)
                return new_room
    
    def make_new_room(self):
        """
        Creates a new room.

        Returns:
            WaitingRoom: The new room.
        """
        new_room_name = "Room " + str(len(self.waiting_rooms) + 1) 
        return WaitingRoom(self, new_room_name)
    
    def make_message(self, type, content):
        """
        Creates a JSON message.

        Args:
            type (str): The type of the message.
            content (str): The content of the message.

        Returns:
            str: The JSON message.
        """
        return json.dumps({'type': type, 'content': content})
    
    def decode_message(self, message):
        """
        Decodes a JSON message.

        Args:
            message (str): The JSON message to decode.

        Returns:
            dict: The decoded message.
        """
        return json.loads(message)

    async def handle_client(self, websocket):
        print(f"Handling new client: {websocket.remote_address}")
        """
        This function handles the server-side websocket connections.
        Args:
            websocket (websockets.WebSocketServerProtocol): The websocket to handle.
        """
        # Add the websocket to the set of connected websockets
        self.connected.add(websocket)
        client_state = "INIT"
        
        while True:
            try:
                await asyncio.sleep(0.05)
                
                if client_state == "INIT":

                    print("In INIT")
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    except asyncio.TimeoutError:
                        print('No message received from client within 1 second')
                        continue  # Continue to the next iteration of the loop
                    player = self.decode_message(message)
                    username = player.get('username')
                    print(f"Received Player: {player}")
                    logging.info(f"Received username...")
                    # find_room = self.make_message('INIT', "Finding a room for you...")
                    # await websocket.send(find_room)
                    print(f"Sent message to {websocket.remote_address}")

                    # ack = await websocket.recv()
                    # # async with self.ack_lock:
                    # await self.ack_queue.put(ack)

                    room = await self.find_available_room(player, websocket)
                    #logging.info(f"Room found for player {player}")
                    print(f"Here is the latest player: {room.players}")
                    await room.broadcast(self.make_message('INIT', room.players))
                    # ack = await websocket.recv()
                    # await self.ack_queue.put(ack)
                    print("Here")
                    if room.has_game_started():
                        client_state = "GAMEPLAY"
                    else:
                        client_state = "WAITING"
                elif client_state == "GAMEPLAY":
                    game_id = self.client_game_map.get(websocket)
                    player_id = player.get('player_id')
                    action_translator = self.action_translators.get(game_id)

                    print("Before...")
                    await action_translator.get_send_game_state_flag().wait()
                    await asyncio.sleep(0.05)
                    print("After...")
                    
                    # async with self.game_states_lock:
                    game_state = self.game_states.get(game_id).get('game_state')
                    print(f"Here is the game state right now: {game_state}")
                    message = self.make_message('gameplay_data', game_state)
                    await websocket.send(message)
                    print(message)
                    response = await websocket.recv()
                    client_response = self.decode_message(response)
                    client_response_type = client_response.get('type')
                    print("Here is the response", client_response, "with type: ", client_response_type)
                    if client_response_type == 'ack':
                        # async with self.game_actions_lock:
                        action_queue = self.game_actions.get(game_id)
                        await action_queue.put(client_response)
                    elif client_response_type == 'action':
                        # async with self.game_actions_lock:
                        action_queue = self.game_actions.get(game_id)
                        client_command = client_response.get('payload')
                        game_action = action_translator.network_to_game_action(client_command, player_id)
                        await action_queue.put(game_action)
                    if action_translator.get_send_game_state_flag().is_set():
                        action_translator.get_send_game_state_flag().clear()
                        print("Flag cleared")

                elif client_state == "WAITING":
                    if room.has_game_started():
                        client_state = "GAMEPLAY"
                
            except Exception as e:
                logging.error(f"Exception in handle_client for player {username}: {str(e)}")
                print(f"Lost connection for player {player}")
                await websocket.close()
                break

    async def monitor_acknowledgements(self):
        """
        Constantly monitors for acknowledgements and logs them when found.
        """
        while True:
            ack = await self.ack_queue.get()  # Dequeue an acknowledgement
            if ack:  # Perform your acknowledgment logic here
                logging.debug(f"Acknowledgement received: {ack}")

    async def start_game(self, room, players, player_sockets):
        """
        Starts a new game.

        Args:
            room (Room): The room where the game will be started.
            players (list): The list of players in the game.
            player_sockets (list): The list of player sockets.
        """
        game_id = self.generate_unique_id()
        async with self.game_actions_lock:
            self.game_actions[game_id] = asyncio.Queue(maxsize=len(players))
        async with self.game_states_lock:
            self.game_states[game_id] = {}
        async with self.action_translators_lock:
            self.action_translators[game_id] = ActionTranslator()
        async with self.game_state_acks_lock:
            self.game_state_acks[game_id] = asyncio.Queue(maxsize=len(players))
        game = Game(players, game_id, self.action_translators.get(game_id), self.game_states.get(game_id), self.game_actions.get(game_id))
        async with self.active_games_lock:
            self.active_games[game_id] = game
        for player_socket in player_sockets:
            self.client_game_map[player_socket] = game.get_game_id()
        room.set_game_started(True)
        asyncio.create_task(self.run_game(game))

    async def run_game(self, game):
        """
        Runs the game loop.

        Args:
            game (Game): The game to run.
        """
        await game.game_loop()

    def start_server(self):
        # Start the websocket server on localhost:8765
        start_server = websockets.serve(self.handle_client, "192.168.86.34", 8765, reuse_port=True)
        # Run the server until it is complete
        asyncio.get_event_loop().run_until_complete(start_server)
        # Start the waiting room monitor
        asyncio.get_event_loop().create_task(self.monitor_waiting_rooms())
        # Start the acknowledgement monitor
        asyncio.get_event_loop().create_task(self.monitor_acknowledgements())
        # Keep the server running forever  
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = WebSocketServer()
    server.start_server()
