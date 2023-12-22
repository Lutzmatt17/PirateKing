// @ts-nocheck
'use client';
import Hero from "@/components/Layout/Hero";
import Join from "@/components/Game/Join";
import React, {useState} from "react";

function HomePage() {
  const [isClicked, setIsClicked] = useState(false);

  const handleClick = (click) => {
    setIsClicked(click)
  }

  return (
    <div className="relative h-screen w-full">
      <Hero onSaveClick={handleClick}/>
      {isClicked && <Join onSaveClick={handleClick}/>}
    </div>
  )
}

export default HomePage;
