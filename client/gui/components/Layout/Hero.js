// @ts-nocheck

import { Fragment } from "react";
import Button from "../UI/Button";

function Hero(props) {

  const playClickHandler = () => {
    props.onSavePlayClick(true)
  }

  const loginClickHandler = () => {
    props.onSaveLoginClick(true)
  }

  return (
    <Fragment>
        <div className="absolute inset-0"></div>
        <div className="bg-cover bg-no-repeat bg-center h-screen w-full bg-[url('/images/OceanicBackground-2.png')] md:bg-[url('/images/OceanicBackground-2.png')]"></div>
        <div className="absolute z-10 inset-0 flex flex-col items-center justify-center space-y-4">
        <h1 className="text-black text-6xl md:text-9xl font-semibold font-pirata">Dead Man's Folly</h1>
            <div className="flex flex-col md:flex-row space-y-2.5 md:space-y-0 md:space-x-2.5">
                <Button onClick={playClickHandler} outerClassname="bg-red-700" innerClassName="bg-red-600">Play Now</Button>
                <Button onClick={loginClickHandler} outerClassname="bg-red-700" innerClassName="bg-red-600">Login</Button>
            </div>
        </div>
    </Fragment>
  )
}

export default Hero;