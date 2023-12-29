'use client'
import React, { useReducer } from 'react';


const initialState = {
  round: 0,
  tricks: {},
  trick: {},
  trickWinner: {},
  phase: "",
  dealer: null,
  bids: {},
  currentPlayer: 0,
  previousPlayer: 0,
  playerNum: 0,
  hands: {},
  scoreSheet: {},
  userName:"",
  players: [],
  countdown: ""
};

const ACTIONS = {
  SET_ROUND: "set-round",
  SET_TRICKS: "set-tricks",
  SET_TRICK: "set-trick",
  SET_TRICK_WINNER: "set-trick-winner",
  SET_PHASE: "set-phase",
  SET_DEALER: "set-dealer",
  SET_BIDS: "set-bids",
  SET_CURRENT_PLAYER: "set-current-player",
  SET_PREVIOUS_PLAYER: "set-previous-player",
  SET_PLAYER_NUM: "set-player-num",
  SET_HANDS: "set-hands",
  SET_SCORE_SHEET: "set-score-sheet",
  SET_USERNAME: "set-username",
  SET_PLAYERS: "set-players",
  SET_COUNTDOWN: "set-countdown"
};

function reducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_ROUND:
      return { ...state, round: action.payload };
    case ACTIONS.SET_TRICKS:
      return { ...state, tricks: action.payload };
    case ACTIONS.SET_TRICK:
      return { ...state, trick: action.payload };
    case ACTIONS.SET_TRICK_WINNER:
      return { ...state, trickWinner: action.payload };
    case ACTIONS.SET_PHASE:
      return { ...state, phase: action.payload };
    case ACTIONS.SET_DEALER:
      return { ...state, dealer: action.payload };
    case ACTIONS.SET_BIDS:
      return { ...state, bids: action.payload };
    case ACTIONS.SET_CURRENT_PLAYER:
      return { ...state, currentPlayer: action.payload };
    case ACTIONS.SET_PREVIOUS_PLAYER:
      return { ...state, previousPlayer: action.payload };
    case ACTIONS.SET_PLAYER_NUM:
      return { ...state, playerNum: action.payload };
    case ACTIONS.SET_HANDS:
      return { ...state, hands: action.payload };
    case ACTIONS.SET_SCORE_SHEET:
      return { ...state, scoreSheet: action.payload };
    case ACTIONS.SET_USERNAME:
      return { ...state, userName: action.payload };
    case ACTIONS.SET_PLAYERS:
      return { ...state, players: action.payload };
    case ACTIONS.SET_COUNTDOWN:
      return { ...state, countdown: action.payload };
    default:
      return state;
  }
}

const UsernameContext = React.createContext(initialState);

export default UsernameContext;

export function UsernameProvider(props) {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <UsernameContext.Provider
      value={{
        round: state.round,
        setRound: (round) => dispatch({ type: ACTIONS.SET_ROUND, payload: round }),
        tricks: state.tricks,
        setTricks: (tricks) => dispatch({ type: ACTIONS.SET_TRICKS, payload: tricks }),
        trick: state.trick,
        setTrick: (trick) => dispatch({ type: ACTIONS.SET_TRICK, payload: trick }),
        trickWinner: state.trickWinner,
        setTrickWinner: (trickWinner) => dispatch({ type: ACTIONS.SET_TRICK_WINNER, payload: trickWinner }),
        phase: state.phase,
        setPhase: (phase) => dispatch({ type: ACTIONS.SET_PHASE, payload: phase }),
        dealer: state.dealer,
        setDealer: (dealer) => dispatch({ type: ACTIONS.SET_DEALER, payload: dealer }),
        bids: state.bids,
        setBids: (bids) => dispatch({ type: ACTIONS.SET_BIDS, payload: bids }),
        currentPlayer: state.currentPlayer,
        setCurrentPlayer: (currentPlayer) => dispatch({ type: ACTIONS.SET_CURRENT_PLAYER, payload: currentPlayer }),
        previousPlayer: state.previousPlayer,
        setPreviousPlayer: (previousPlayer) => dispatch({ type: ACTIONS.SET_PREVIOUS_PLAYER, payload: previousPlayer }),
        playerNum: state.playerNum,
        setPlayerNum: (playerNum) => dispatch({ type: ACTIONS.SET_PLAYER_NUM, payload: playerNum }),
        hands: state.hands,
        setHands: (hands) => dispatch({ type: ACTIONS.SET_HANDS, payload: hands }),
        scoreSheet: state.scoreSheet,
        setScoreSheet: (scoreSheet) => dispatch({ type: ACTIONS.SET_SCORE_SHEET, payload: scoreSheet }),
        userName: state.userName,
        setUsername: (userName) => dispatch({ type: ACTIONS.SET_USERNAME, payload: userName }),
        players: state.players,
        setPlayers: (players) => dispatch({ type: ACTIONS.SET_PLAYERS, payload: players }),
        countdown: state.countdown,
        setCountdown: (countdown) => dispatch({ type: ACTIONS.SET_COUNTDOWN, payload: countdown })
      }}
    >
      {props.children}
    </UsernameContext.Provider>
  );
}
