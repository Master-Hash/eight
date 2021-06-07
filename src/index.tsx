import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props: {value: null | "x" | "o", onClick: any}) {
  return (
    <button
      className="square"
      onClick={props.onClick}
    >
      {props.value ? props.value.toUpperCase() : ""}
    </button>
  );
}

function Board(props: any) {
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [round, setRound] = useState(0);
  let status = `Next player: ${round & 1 ? "O" : "X"}`;
  const winner = calculateWinner(squares);
  if (winner) {
    status = 'Winner: ' + winner;
  }

  function handleClick(i: number) {
    if (winner) { return; }
    const newSquares = squares.slice();
    newSquares[i] = round & 1 ? "o" : "x";
    setSquares(newSquares);
    setRound(round + 1);
  }

  function renderSquare(i: number) {
    return (
      <Square
        value={squares[i]}
        onClick={() => handleClick(i)}
      />
    );
  }

  return (
    <div>
      <div className="status">{status}</div>
      <div className="board-row">
        {renderSquare(0)}
        {renderSquare(1)}
        {renderSquare(2)}
      </div>
      <div className="board-row">
        {renderSquare(3)}
        {renderSquare(4)}
        {renderSquare(5)}
      </div>
      <div className="board-row">
        {renderSquare(6)}
        {renderSquare(7)}
        {renderSquare(8)}
      </div>
    </div>
  );
}

function Game(props: any) {
  return (
    <div className="game">
      <div className="game-board">
        <Board />
      </div>
      <div className="game-info">
        <div>{/* status */}</div>
        <ol>{/* TODO */}</ol>
      </div>
    </div>
  );
}

function calculateWinner(squares: Array<null | "x" | "o">) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

// ========================================

ReactDOM.render(
  <Game />,
  document.querySelector('#root')
);
