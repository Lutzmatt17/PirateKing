import React, { useEffect, useState } from 'react';
import GameCard from '@/components/Game/GameCard';

function GameBoard() {
    const [dealCards, setDealCards] = useState(false);
    const initialCards = [
        {id: 1, transitioned: false, type: "Parrot"},
        {id: 2, transitioned: false, type: "Pirate Map"},
        {id: 3, transitioned: false, type: "Treasure Chest"},
        {id: 4, transitioned: false, type: "Jolly Roger"},
        {id: 5, transitioned: false, type: "Pirate"},
        {id: 6, transitioned: false, type: "Escape"},
        {id: 7, transitioned: false, type: "Tigress"},
        {id: 8, transitioned: false, type: "Skull King"}
    ]
    const [cards, setCards] = useState(initialCards);

    useEffect(() => {
      const timer = setTimeout(() => {
        setDealCards(true);
      }, 1); // Delay the state change
      
      return () => clearTimeout(timer); // Clean up on unmount
    }, []);

    useEffect(() => {
        const timers = cards.map((card, index) => {
          return setTimeout(() => {
            setCards(prevCards => {
              return prevCards.map(item => 
                item.id === card.id ? { ...item, transitioned: true } : item
              );
            });
          }, (index + 1) * 115); // Adjust timing as needed
        });
    
        // Cleanup
        return () => timers.forEach(timer => clearTimeout(timer));
      }, []);
    
  
    return (
      <div className="relative bg-cover bg-[url('/images/PlankBackground.png')] h-screen w-full flex justify-center items-center"> 
          <div className='absolute inset-0 flex justify-center items-center -space-x-40'>
          {cards.map((card, index) => (
                  <GameCard 
                      key={index} 
                      delay={index*100}
                      className={`transition-transform duration-500 ease-out ${dealCards ? 'opacity-100' : 'opacity-0'}`} 
                      style={{ 
                        zIndex: card.transitioned ? index : cards.length - index, 
                        transitionDelay: `${index * 125}ms`,
                        transform: dealCards ? `translateY(150%) translateX(${(index - cards.length / 2) * 100}px)` : 'translateY(0) translateX(0)'
                      }} 
                      type={card.type}
                  />
              ))}
          </div>
      </div>
    )
  }

export default GameBoard;