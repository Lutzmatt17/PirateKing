// @ts-nocheck
'use client';
import { Fragment } from "react";
import Button from "../UI/Button";

function Hero(props) {

  const playClickHandler = () => {
    props.onSaveClick(true)
  }

  return (
    <Fragment>
        <div className="absolute inset-0 bg-blue-500"></div>
        <div className="bg-cover bg-[url('/images/PirateKing.png')] h-screen w-full"></div>
        <div className="absolute z-10 inset-0 flex flex-col items-center justify-center space-y-4">
        <h1 className="text-black text-9xl font-semibold font-serif">Pirate King</h1>
            <div className="flex space-x-2.5">
                <Button onClick={playClickHandler} outerClassname="bg-red-700" innerClassName="bg-red-600">Play Now</Button>
                <Button onClick={playClickHandler} outerClassname="bg-red-700" innerClassName="bg-red-600">Login</Button>
            </div>
        </div>
    </Fragment>
  )
}

export default Hero;