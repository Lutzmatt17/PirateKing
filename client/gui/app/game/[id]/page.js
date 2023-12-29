// @ts-nocheck
'use client'
import GameBoard from '@/components/Game/GameBoard';
import GameBoardTest from '@/components/Game/GameBoardTest';

const CARD_TYPES = [
  "Parrot",
  "Pirate Map",
  "Treasure Chest",
  "Jolly Roger",
  "Pirate",
  "Escape",
  "Tigress",
  "Skull King"
];

function GamePage() {
  
  return (
    <GameBoard/>
  )
}

export default GamePage;