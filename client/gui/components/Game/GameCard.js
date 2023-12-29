import React, { useState, useEffect } from 'react'
import './GameCard.css'

const CARD_TYPES = {
  PARROT: "Parrot",
  PIRATE_MAP: "Pirate Map",
  TREASURE_CHEST: "Treasure Chest",
  JOLLY_ROGER: "Jolly Roger",
  PIRATE: "Pirate",
  ESCAPE: "Escape",
  TIGRESS: "Tigress",
  SKULL_KING: "Skull King",
  KRAKEN: "Kraken",
  WHITE_WHALE: "White Whale",
  MERMAID: "Mermaid",
  DEAD_MAN: "Dead Mans Folly"
}

const CARD_NUMBERS = {
  ONE: "1",
  TWO: "2",
  THREE: "3",
  FOUR: "4",
  FIVE: "5",
  SIX: "6",
  SEVEN: "7",
  EIGHT: "8",
  NINE: "9",
  TEN: "10",
  ELEVEN: "11",
  TWELVE: "12",
  THIRTEEN: "13",
  FOURTEEN: "14"
}

function GameCard(props) {
  const [card, setCard] = useState("");
  const [number, setNumber] = useState("");
  const [bonus, setBonus] = useState("");
  const [isFlipped, setIsFlipped] = useState(true);

  useEffect(() => {
    switch (props.type) {
      case CARD_TYPES.PARROT:
        setCard("/images/cards/Parrot.png");
        break;
      case CARD_TYPES.PIRATE_MAP:
        setCard("/images/cards/PirateMap.png");
        break;
      case CARD_TYPES.TREASURE_CHEST:
        setCard("/images/cards/TreasureChest.png");
        break;
      case CARD_TYPES.JOLLY_ROGER:
        setCard("/images/cards/JollyRoger.png");
        break;
      case CARD_TYPES.PIRATE:
        setCard("/images/cards/Pirate.png");
        break;
      case CARD_TYPES.ESCAPE:
        setCard("/images/cards/Escape.png");
        break;
      case CARD_TYPES.TIGRESS:
        setCard("/images/cards/Tigress.png");
        break;
      case CARD_TYPES.SKULL_KING:
        setCard("/images/cards/SkullKing.png");
        break;
      case CARD_TYPES.KRAKEN:
        setCard("/images/cards/Kraken.png");
        break;
      case CARD_TYPES.WHITE_WHALE:
        setCard("/images/cards/WhiteWhale.png");
        break;
      case CARD_TYPES.MERMAID:
        setCard("/images/cards/Mermaid.png");
        break;
      case CARD_TYPES.DEAD_MAN:
        setCard("/images/cards/DeadMansFolly.png")
        break;
      default:
        setCard("");
    }

    switch (props.number) {
      case CARD_NUMBERS.ONE:
      case CARD_NUMBERS.TWO:
      case CARD_NUMBERS.THREE:
      case CARD_NUMBERS.FOUR:
      case CARD_NUMBERS.FIVE:
      case CARD_NUMBERS.SIX:
      case CARD_NUMBERS.SEVEN:
      case CARD_NUMBERS.EIGHT:
      case CARD_NUMBERS.NINE:
      case CARD_NUMBERS.TEN:
      case CARD_NUMBERS.ELEVEN:
      case CARD_NUMBERS.TWELVE:
      case CARD_NUMBERS.THIRTEEN:
        setNumber(props.number);
        setBonus("0");
        break;
      case CARD_NUMBERS.FOURTEEN:
        setNumber(props.number);
        setBonus("10");
        break;
      default:
        setNumber("");
        setBonus("");
    }
  }, [props.type, props.number]);

  const numberCSS = `absolute p-1 text-xl text-black font-serif font-semibold 
                    ${props.type === 'Jolly Roger' ? 'text-yellow-500' : ''} `                  


  useEffect(() => {
    const timer = setTimeout(() => {
      setIsFlipped(!isFlipped);
    }, shortDelay); // Delay the state change

    return () => clearTimeout(timer); // Clean up on unmount
  }, []);

  const longDelay = 4500 + Number(props.delay);
  const shortDelay = 1600 + Number(props.delay);
  
  return (
    <div style={props.style} className={"w-40 relative " + props.className} >
        <div className={`flip-card ${isFlipped ? 'flipped' : ''}`}>
          <div className="flip-card-inner">
            <div className="flip-card-front shadow-2xl">
              <img className="rounded-xl" src={card} alt="Game Card" />
              {number && (
                <>
                  <div className={numberCSS + 'top-0 left-0'}>
                    {number}
                  </div>
                  <div className={numberCSS + "bottom-0 right-0"}>
                    {number}
                  </div>
                </>
              )}
            </div>
            <div className="flip-card-back">
                <img className="rounded-xl" src="/images/cards/DeadMansFolly.png" alt="Game Card" />
            </div>
          </div>
        </div>
    </div>
  )
}

export default GameCard;