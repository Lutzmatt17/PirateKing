// @ts-nocheck
'use client';
import Hero from "@/components/Layout/Hero";
import Join from "@/components/Game/Join";
import Login from "@/components/Login/Login";
import { UsernameProvider } from "@/components/Context/username-context";
import React, {useState} from "react";

function HomePage() {
  const [isPlayClicked, setIsPlayClicked] = useState(false);
  const [isLoginClicked, setIsLoginClicked] = useState(false)

  const handlePlayClick = (click) => {
    setIsPlayClicked(click)
  }
  const handleLoginClick = (click) => {
    setIsLoginClicked(click)
  }

  return (
    // <UsernameProvider>
      <div className="relative h-screen w-full">
        <Hero onSaveLoginClick={handleLoginClick} onSavePlayClick={handlePlayClick}/>
        {isPlayClicked && <Join className="mt-36" onSavePlayClick={handlePlayClick}/>}
        {isLoginClicked && <Login className="mt-32" onSaveLoginClick={handleLoginClick} />}
      </div>
    /* </UsernameProvider> */
  )
}

export default HomePage;
