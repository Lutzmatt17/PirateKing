import socket
import time
from player import Player
import threading
import json
import logging
from datetime import datetime
import uuid

logging.basicConfig(level=logging.DEBUG)

class Client:
    servers = {'Laptop': "172.28.5.101",
               'Desktop': "192.168.86.34"}
    laptop = servers.get('Laptop')
    desktop = servers.get('Desktop')
    def __init__(self):
        username = input("Please enter your username: ")
        self.player = Player(username)
        self.game_event = None
        self.server = self.desktop
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect_to_server()
        
    def connect_to_server(self):
            try:
                self.client.connect(self.addr)
            except socket.error as e:
                logging.error(f"Socket error: {str(e)}")
                time.sleep(5)

    def set_game_event(self, game_event):
        self.game_event = game_event
    
    # def send_chat_message(self):
    #      while True:
    #         message = input()
    #         self.client.send(message.encode())

    def receive_message(self):
        #  self.client.settimeout(5)  # Set timeout to 5 seconds
         while True:
            try:
                # logging.info(f"About to receive message data...")
                received_data = self.receive_with_length(self.client)

                if not received_data:
                    print("No data received.")
                    break

                message = self.decode_message(received_data)
                # logging.info(f"Message data received...")
                message_type = message['type']
                content = message['content']

                if message_type not in ['INIT', 'message', 'countdown', 'gameplay_data']:
                     print('Invalid message type')
                     continue
                
                match message_type:
                    case 'countdown':
                        print(f"Game starting in: {content}", end='\r')
                    case 'INIT':
                        self.send_acknowledgment(self.client, "Message received")
                        print(content)
                    case 'message':
                        print(content)
                    case 'gameplay_data':
                        try:
                            processed_state = self.process_state(content)
                            if processed_state:
                                message = self.make_message(processed_state)
                                self.send_acknowledgment(self.client, message)
                        except socket.error as e:
                            print(f"Failed to send data: {e}")

                        
            except socket.error as e:
                 print("Socket error " + str(e))
                 break
    
    def send_message(self):
        while True:
            user_input = input()
            message = {'type': 'action', 'payload': user_input}
            command_to_send = self.make_message(message)
            self.send_with_length(self.client, command_to_send)
    
    def decode_message(self, message):
        #  print(message)
         return json.loads(message)

    def send_with_length(self, client_socket, message):
        message_length = str(len(message))
        # Pad with zeros to make it a 4-byte length prefix
        message_length = message_length.zfill(4)
        # Concatenate the length prefix and the actual message
        full_message = message_length + message
        try:
            sent = client_socket.send(full_message.encode())
            logging.info(f"This is the number of bytes that was sent: {sent}")
        except BrokenPipeError as e:
            logging.error(f"Client disconnected because: {str(e)}")
            client_socket.close()

    def receive_with_length(self, client_socket):
        message_length = int(client_socket.recv(4).decode())
        message = client_socket.recv(message_length).decode()
        return message

    def send_acknowledgment(self, client_socket, ack):
        try:
            # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.send_with_length(client_socket, ack)
            # logging.info(f"Sent ack at: {current_time}")
        except socket.error as e:
            print(f"Failed to send acknowledgment: {str(e)}")

    def make_message(self, message):
        return json.dumps(message)
    def process_state(self, state):

        phase = state.get('phase')
        ack = "Game State Processed"
        if phase == "STARTING":
            round = state.get('round')
            print(f"Game is starting with round: {round}")
            return {'type': 'ack', 'payload': ack}
        elif phase == "DEALING":
            print(f"Dealing cards...")
            hands = state.get('hands')
            player_hand = hands.get(self.player.get_player_id())
            # print(f"This is your hand: {player_hand}")
            self.player.set_hand(player_hand)
            self.player.print_hand()
            return {'type': 'ack', 'payload': ack}
        elif phase == "START_BIDDING":
            print("Please enter your bid: ")
        elif phase == "BIDDING":
            bids = state.get('bids')
            print(bids)
            return {'type': 'ack', 'payload': ack}
        elif phase == "START_PLAYING":
            first_player = state.get('first_player')
            first_player_username = first_player.get('username')
            if first_player_username == self.player.get_username():
                print("Your turn, please play a card: ")
            else:
                print(f"{first_player_username}'s turn!")
                return {'type': 'ack', 'payload': ack}

        elif phase == "PLAYING":
            previous_player = state.get('previous_player')
            previous_player_username = previous_player.get('username')
            current_player = state.get('current_player')
            current_player_username = current_player.get('username')
            trick = state.get('trick')
            player_num = state.get('player_num')
            card = list(trick.values())[-1]
            print(f"{previous_player_username}, played {card}")
            if len(trick) < player_num:
                if current_player_username == self.player.get_username():
                    print("Your turn, please play a card: ")
                else:
                    print(f"{current_player_username}'s turn!")
                    return {'type': 'ack', 'payload': ack}
            else:
                return {'type': 'ack', 'payload': ack}

        elif phase == "RESOLVING":
            winner = state.get('trick_winner')
            winner_name = winner.get('username')
            print(f"{winner_name} won this trick!")
            hands = state.get('hands')
            player_hand = hands.get(self.player.get_player_id())
            # print(f"This is your hand: {player_hand}")
            self.player.set_hand(player_hand)
            self.player.print_hand()
            return {'type': 'ack', 'payload': ack}
        
        elif phase == "CALCULATE_SCORES":
            score_sheet = state.get('score_sheet')
            print(f"Here are the scores for this round: {score_sheet}")
            return {'type': 'ack', 'payload': ack}

    # def receive(self):
    #     return self.client.recv(2048).decode()
    
    def run(self):
        # logging.info(f"Sending username...")
        player = json.dumps(self.player.to_dict())
        
        self.send_with_length(self.client, player)
        # logging.info(f"Sent username")
        send_thread = threading.Thread(target=self.send_message)
        receive_thread = threading.Thread(target=self.receive_message)
        send_thread.start()
        receive_thread.start()
    
        
       
    # def enable_chat(self):
    #     send_thread = threading.Thread(target=self.send_message)
    #     receive_thread = threading.Thread(target=self.receive_message)
    #     send_thread.start()
    #     receive_thread.start()

class ClientDriver:
    
    def main(self):
        self.client = Client()
        self.client.run()

if __name__ == "__main__":
        client_driver = ClientDriver()
        client_driver.main()

    