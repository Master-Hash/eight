import React, { useState } from 'react';

// function

// function Hand(props) {
//   return ();
// }

interface Round {
  round: number
}

interface Hands {
  hands: {
    green: number[]
    pink: number[]
  }
}

function Color(props: {color: "green" | "pink", content: string}) {
  return <span className={props.color}>{props.content}</span>
}

function Notice(props: Round) {
  const round = props.round & 1 ? "pink" : "green";
  return (
    <div className="notice">
      轮到<Color color={round} content={props.round & 1 ? "粉" : "绿"}></Color>了！
    </div>
  );
}

function Board(props: Round & Hands) {
  return (
    <div className="board">
      <div className="green">
        <button className="right-hand">{props.hands.green[1]}</button>
        <button className="left-hand">{props.hands.green[0]}</button>
      </div>
      <hr />
      <div className="pink">
        <button className="left-hand">{props.hands.pink[0]}</button>
        <button className="right-hand">{props.hands.pink[1]}</button>
      </div>
    </div>
  );
}

function History(props: any) {
  return (
    <div className="history">

    </div>
  );
}

export default function Game(props: any) {
  const [round, setRound] = useState(0);
  const [hands, setHands] = useState({
    green: [1, 1],
    pink: [1, 1],
  });
  return (
    <main>
      <Notice round={round} />
      <Board round={round} hands={hands} />
      <History />

    </main>
  );
}
