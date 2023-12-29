import React, { useEffect, useState } from 'react';
import GameCard from '@/components/Game/GameCard';

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

function GameBoardTest() {
    const [deck, setDeck] = useState([...CARD_TYPES]);
    const [hand, setHand] = useState([]);
    const [dealCards, setDealCards] = useState(false);

    useEffect(() => {
      if (deck.length > 0) {
        const timer = setTimeout(() => {
          setHand((prevHand) => [...prevHand, deck[0]]);
          setDeck((prevDeck) => prevDeck.slice(1));
        }, 500); // Deal a card every 500ms
        setDealCards(true)
        return () => clearTimeout(timer); // Clean up on unmount
        
      }
      
    }, [deck]);
    
    return (
      <div className="relative bg-cover bg-[url('/images/OceanicBackground-2.png')] h-screen w-full flex justify-center items-center"> 
          <div className="absolute inset-0 flex justify-center items-center">
              <div style={{ boxShadow: 'inset 0px 0px 4px 2px rgba(0, 0, 0, 0.6)' }} 
                   className="bg-[url('/images/PlankBackground.png')] w-full h-full">
                  <div className='absolute inset-0 flex justify-center items-center -space-x-40'>
                    {deck.map((type, index) => (
                            <GameCard 
                                key={index} 
                                delay={index*100}
                                className={`transition-transform duration-1000 ease-out ${dealCards ? 'opacity-100' : 'opacity-0'}`} 
                                style={{ 
                                  zIndex: CARD_TYPES.length - index, 
                                  transitionDelay: `${index * 500}ms`,
                                  transform: dealCards ? `translateY(150%) translateX(${(index - CARD_TYPES.length / 2) * 100}px)` : 'translateY(0) translateX(0)'
                                }} 
                                type={type}
                            />
                        ))}
                    
                    </div> 
                    <div className='absolute inset-0 flex justify-center items-center -space-x-10'>         
                    {hand.map((type, index) => (
                            <GameCard 
                                key={index} 
                                delay={index*100}
                                type={type}
                            />
                        ))}
                    </div>  
                  
              </div>
          </div>
      </div>
    )
  }

export default GameBoardTest;