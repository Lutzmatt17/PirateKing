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
    def __init__(self):
        username = input("Please enter your username: ")
        self.player = Player(username)
        self.server = "172.28.5.101"
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
                            # logging.info(f"Received Hand: {content}")
                            # self.send_acknowledgment(self.client, "Gameplay data received")
                            self.player.set_hand(content)
                            self.player.print_hand()  
                        except socket.error as e:
                            print(f"Failed to send data: {e}")

                        
            except socket.error as e:
                 print("Socket error " + str(e))
                 break
    
    def send_message(self):
        while True:
            message = input()
            self.send_with_length(self.client, message)
    
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
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.send_with_length(client_socket, ack)
            logging.info(f"Sent ack at: {current_time}")
        except socket.error as e:
            print(f"Failed to send acknowledgment: {str(e)}")

    def create_command(self, command_string):
        command = command_string.split()
        command_type = command[0]

        if command_type == "/play":
            card_index = int(command[1])
            card = self.player.get_hand()[card_index]
            command_type = "PLAY_CARD"
            command_dict = {"type": command_type, "player_id": self.player.get_player_id(), "data": card}
        elif command_type =="/bid":
            bid = int(command[1])
            command_type = "BID"
            command_dict = {"type": command_type, "player_id": self.player.get_player_id(), "data": bid}
        elif command_type == "/show":
            command_type = "SHOW"
            command_dict = {"type": command_type, "player_id": self.player.get_player_id(), "data": self.player.get_hand()}
        return command_dict

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

    