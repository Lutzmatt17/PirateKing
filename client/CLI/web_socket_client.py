import asyncio
import websockets
import json
from player import Player

class WebSocketClient:
    def __init__(self, uri="ws://192.168.86.34:8765"):
        self.uri = uri
        self.websocket = None
        username = input("Please enter your username: ")
        self.player = Player(username)
      
    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        
    async def receive_message(self):
        while True:
            try:
                # logging.info(f"About to receive message data...")
                received_data = await self.websocket.recv()

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
                        # await self.send_acknowledgment("Message received")
                        print(content)
                    case 'message':
                        print(content)
                    case 'gameplay_data':
                        try:
                            processed_state = self.process_state(content)
                            if processed_state:
                                message = self.make_message(processed_state)
                                print(message)
                                await self.send_acknowledgment(message)
                                print("Ack Sent")
                        except Exception as e:
                            print(f"Failed to send data: {e}")
            except Exception as e:
                print("Socket error " + str(e))
                break
    
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
    
    async def send_message(self):
        """
        This function is responsible for sending a message from the client to the server.
        It continuously takes user input and sends it as a message of type 'action'.
        """
        loop = asyncio.get_event_loop()
        while True:
            user_input = await loop.run_in_executor(None, input)  # Get user input
            message = {'type': 'action', 'payload': user_input}  # Construct message
            command_to_send = json.dumps(message)  # Convert message to JSON
            await self.websocket.send(command_to_send)  # Send message with websocket
    
    async def send_acknowledgment(self, ack):
        try:
            # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            await self.websocket.send(ack)
            # logging.info(f"Sent ack at: {current_time}")
        except Exception as e:
            print(f"Failed to send acknowledgment: {str(e)}")

    def decode_message(self, message):
        """
        This function decodes a JSON message.
        Args:
            message (str): The message to decode.
        Returns:
            dict: The decoded message.
        """
        return json.loads(message)

async def main():
    client = WebSocketClient()
    player = json.dumps(client.player.to_dict())
    await client.connect()
    asyncio.create_task(client.send_message())
    await client.websocket.send(player)
    await client.receive_message()
    
asyncio.get_event_loop().run_until_complete(main())
