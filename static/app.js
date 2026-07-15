// The browser draws the board; Python remains the authority on every rule.
const svg = document.querySelector("#board");
const pieces = document.querySelector("#pieces");
const statusText = document.querySelector("#status");
const timerText = document.querySelector("#timer");
const modeSelect = document.querySelector("#mode");
const levelSelect = document.querySelector("#difficulty");
const SVG_NS = "http://www.w3.org/2000/svg";
const positions = [[10,10],[50,10],[90,10],[20,20],[50,20],[80,20],[30,30],[50,30],[70,30],[10,50],[20,50],[30,50],[70,50],[80,50],[90,50],[30,70],[50,70],[70,70],[20,80],[50,80],[80,80],[10,90],[50,90],[90,90]];
let state;
let selectedSource = null;
let turnStartedAt = Date.now();
let clock;
let lastSnore = -1;
let audioContext;

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) alert(data.error);
  return data.state || data;
}

function playerName(player) { return player === 0 ? "Red" : "Blue"; }
function humanTurn() { return state.mode === "local" || state.turn === 0; }
function status() {
  if (state.winner !== null) return `${playerName(state.winner)} wins!`;
  if (state.must_remove) return `${playerName(state.turn)} formed a mill — remove a highlighted piece.`;
  return state.reserve[state.turn] > 0 ? `${playerName(state.turn)}: place a piece.` : `${playerName(state.turn)}: select a piece, then a destination.`;
}

function ensureAudio() {
  audioContext ||= new (window.AudioContext || window.webkitAudioContext)();
  if (audioContext.state === "suspended") audioContext.resume();
}

function snore() {
  // A short low-pitched sound: browsers allow this only after a player click.
  if (!audioContext) return;
  const now = audioContext.currentTime;
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  oscillator.type = "sawtooth";
  oscillator.frequency.setValueAtTime(100, now);
  oscillator.frequency.exponentialRampToValueAtTime(55, now + 0.65);
  gain.gain.setValueAtTime(0.001, now);
  gain.gain.exponentialRampToValueAtTime(0.12, now + 0.08);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.75);
  oscillator.connect(gain).connect(audioContext.destination);
  oscillator.start(); oscillator.stop(now + 0.76);
}

function restartClock() {
  clearInterval(clock);
  turnStartedAt = Date.now();
  lastSnore = -1;
  clock = setInterval(() => {
    if (!state || state.winner !== null || !humanTurn()) { timerText.textContent = "—"; return; }
    const seconds = Math.floor((Date.now() - turnStartedAt) / 1000);
    const left = Math.max(0, 30 - seconds);
    timerText.textContent = `0:${String(left).padStart(2, "0")}`;
    timerText.classList.toggle("calm", left > 5);
    // Start after 30 seconds and repeat every 3 seconds until a move is made.
    const snoreNumber = seconds >= 30 ? Math.floor((seconds - 30) / 3) : -1;
    if (snoreNumber > lastSnore) { lastSnore = snoreNumber; snore(); }
  }, 250);
}

function addNode(index, piece) {
  const node = document.createElementNS(SVG_NS, "g");
  const classes = ["node"];
  if (piece === null) classes.push("empty");
  else classes.push(piece === 0 ? "red" : "blue");
  if (index === selectedSource) classes.push("selected");
  if (state.must_remove && state.removable.includes(index)) classes.push("removable");
  if (piece === null && !state.must_remove && humanTurn()) classes.push("empty-target");
  node.setAttribute("class", classes.join(" "));
  node.setAttribute("transform", `translate(${positions[index][0]} ${positions[index][1]})`);
  node.setAttribute("role", "button");
  node.setAttribute("aria-label", `Board position ${index}`);
  const circle = document.createElementNS(SVG_NS, "circle");
  circle.setAttribute("r", "4.3");
  node.append(circle);
  node.onclick = () => choosePosition(index);
  pieces.append(node);
}

function render() {
  pieces.innerHTML = "";
  state.board.forEach(addNode);
  statusText.textContent = status();
  modeSelect.value = state.mode;
  levelSelect.value = state.difficulty;
  levelSelect.disabled = state.mode === "local";
  document.querySelector("#red-count").textContent = state.reserve[0] + state.board.filter(x => x === 0).length;
  document.querySelector("#blue-count").textContent = state.reserve[1] + state.board.filter(x => x === 1).length;
  document.querySelector("#move-count").textContent = state.move_count;
  const advice = document.querySelector("#recommendation");
  if (state.recommendation && state.winner !== null) {
    const item = state.recommendation;
    advice.hidden = false;
    advice.innerHTML = `A good next move: try this ${item.type}: <a href="${item.url}" target="_blank" rel="noopener">${item.title}</a>.`;
  } else advice.hidden = true;
  restartClock();
}

async function choosePosition(position) {
  if (state.winner !== null || !humanTurn()) return;
  ensureAudio();
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

async function newGame() {
  state = await request("/api/new", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({mode:modeSelect.value, difficulty:+levelSelect.value})});
  selectedSource = null;
  render();
}

document.querySelector("#new-game").onclick = newGame;
modeSelect.onchange = newGame;
levelSelect.onchange = newGame;
request("/api/state").then(data => { state = data; render(); });
