// @ts-nocheck
'use client';
import { useRouter} from 'next/navigation';
import { Fragment, useContext } from 'react';
import JoinRoom from './JoinRoom';
import UsernameContext from '@/components/Context/username-context';


function WaitingRoom() {
  const userNameContext = useContext(UsernameContext);
  const router = useRouter();

  if (userNameContext.countdown === "00:00") {
    router.push("/game/id-1")
  }
  
  return (
    <div className="bg-cover bg-[url('/images/OceanicBackground-2.png')] h-screen w-full
                    flex flex-col justify-center items-center space-y-10">
      <h1 className="text-white text-5xl font-bold">Lobby</h1>
      <div className="flex flex-col space-y-6 w-full items-center">
        {userNameContext.players.map((player, index) => (
            <JoinRoom key={index} number={index + 1} userName={player.username}/>
        ))}
      </div>
        {userNameContext.countdown && 
        <h1 className="text-white text-3xl font-bold mt-18">
          Game Starting in: {userNameContext.countdown}
        </h1>}
    </div>
  );
}

export default WaitingRoom;