// @ts-nocheck
import Modal from "../UI/Modal"
import Button from "../UI/Button";
import React, {useState, useContext, Fragment} from "react";
import { useRouter} from 'next/navigation';
import UsernameContext from '../Context/username-context'
import {v4 as uuidv4} from 'uuid';
import { initiateConnection } from "../Connect/WebSocket";

function Join(props) {
  const userNameContext = useContext(UsernameContext);
  const router = useRouter();

  const handleInputChange = (event) => {
    userNameContext.setUsername(event.target.value)
  }

  const joinClickHandler = () => {

      const socket = initiateConnection();
  
      socket.onopen = () => {
        // Send player data after connection
        socket.send(JSON.stringify({'username': userNameContext.userName, 'player_id': uuidv4()}));
      };

      socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (Array.isArray(message.content)) {
          userNameContext.setPlayers(message.content);
        }
        else if (message.type === "countdown") {
          userNameContext.setCountdown(message.content)
        }
      }
      
      router.push("/room/id-1")
  }

  return (
    <Modal 
      onSavePlayClick={props.onSavePlayClick} 
      className={"bg-blue-600 flex flex-col items-center justify-center space-y-10 " + props.className}
    >
        <input 
            className="w-full rounded-full border-4 border-gray-300 py-2 px-4 text-gray-700 leading-tight 
                       focus:outline-none focus:bg-white focus:border-blue-500" 
            type="text" 
            placeholder="Enter Username" 
            onChange={handleInputChange}
        />
        <Button onClick={joinClickHandler} outerClassname="bg-yellow-500" innerClassName="bg-yellow-400">Join Game</Button>
    </Modal>
  )
}

export default Join;