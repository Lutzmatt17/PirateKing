// @ts-nocheck
import React from 'react'

function JoinRoom(props) {
  return (
    <div className="flex justify-between border-b-4 border-white w-1/3">
      <span className="text-2xl font-semibold"> {props.userName}</span>
      <span className="text-2xl font-semibold">{props.number}</span>
    </div>
  )
}

export default JoinRoom;