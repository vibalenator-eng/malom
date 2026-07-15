// This file only handles the display and clicks. Python validates every rule.
const board = document.querySelector("#board");
const statusText = document.querySelector("#status");
let state;
let selectedSource = null;

// The 24 board positions are laid out on a 7 by 7 CSS grid.
const positions = [
  [1,1],[1,4],[1,7],[2,2],[2,4],[2,6],[3,3],[3,4],[3,5],
  [4,1],[4,2],[4,3],[4,5],[4,6],[4,7],[5,3],[5,4],[5,5],
  [6,2],[6,4],[6,6],[7,1],[7,4],[7,7],
];

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) alert(data.error);
  return data.state || data;
}

function playerName(player) { return player === 0 ? "Red" : "Blue"; }

function updateStatus() {
  if (state.winner !== null) return `${playerName(state.winner)} wins! Start a new game to play again.`;
  if (state.must_remove) return `${playerName(state.turn)} formed a mill — remove a highlighted piece.`;
  return state.reserve[state.turn] > 0
    ? `${playerName(state.turn)}: place a piece.`
    : `${playerName(state.turn)}: select a piece, then a destination.`;
}

function render() {
  board.innerHTML = "";
  state.board.forEach((piece, index) => {
    const node = document.createElement("button");
    node.className = "node";
    node.style.gridArea = `${positions[index][0]} / ${positions[index][1]}`;
    if (piece !== null) node.classList.add(piece === 0 ? "red" : "blue");
    if (index === selectedSource) node.classList.add("selected");
    if (state.must_remove && state.removable.includes(index)) node.classList.add("removable");
    if (piece === null && !state.must_remove) node.classList.add("empty-target");
    node.setAttribute("aria-label", `Board position ${index}`);
    node.onclick = () => choosePosition(index);
    board.append(node);
  });
  statusText.textContent = updateStatus();
  document.querySelector("#red-count").textContent = state.reserve[0] + state.board.filter(x => x === 0).length;
  document.querySelector("#blue-count").textContent = state.reserve[1] + state.board.filter(x => x === 1).length;
  document.querySelector("#move-count").textContent = state.move_count;
}

async function choosePosition(position) {
  if (state.winner !== null) return;
  if (state.must_remove) {
    state = await request("/api/action", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({kind:"remove", position}) });
  } else if (state.reserve[state.turn] > 0) {
    state = await request("/api/action", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({kind:"place", destination:position}) });
  } else if (selectedSource === null && state.board[position] === state.turn) {
    selectedSource = position;
  } else if (selectedSource !== null) {
    state = await request("/api/action", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({kind:"move", source:selectedSource, destination:position}) });
    selectedSource = null;
  }
  render();
}

document.querySelector("#new-game").onclick = async () => { state = await request("/api/new", {method:"POST"}); selectedSource = null; render(); };
request("/api/state").then(data => { state = data; render(); });
