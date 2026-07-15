"""Flask web server for the Malom learning project."""

from __future__ import annotations

from random import choice

from flask import Flask, jsonify, render_template, request

from ai import apply_action, choose_action
from game_engine import GameState, InvalidMove

app = Flask(__name__)
game = GameState()  # Kept in memory: perfect for a local learning project.
mode = "computer"
difficulty = 3
recommendation: dict[str, str] | None = None

FREE_LEARNING_RESOURCES = (
    {"title": "Astronomy 2e", "type": "free science textbook", "url": "https://openstax.org/details/books/astronomy-2e"},
    {"title": "Psychology 2e", "type": "free psychology textbook", "url": "https://openstax.org/details/books/psychology-2e"},
    {"title": "The Art of War", "type": "free public-domain strategy book", "url": "https://www.gutenberg.org/ebooks/132"},
    {"title": "How to Live on 24 Hours a Day", "type": "free public-domain self-development book", "url": "https://www.gutenberg.org/ebooks/2274"},
    {"title": "The Happiness Lab", "type": "free science podcast", "url": "https://www.happinesslab.fm/"},
)


def response_state() -> dict[str, object]:
    """Add web-app settings to the pure game-engine state."""
    state = game.as_dict()
    state.update({"mode": mode, "difficulty": difficulty, "recommendation": recommendation})
    return state


def play_computer_turn() -> None:
    """Make Blue's move(s), including a removal after it forms a mill."""
    while mode == "computer" and game.turn == 1 and game.winner is None:
        apply_action(game, choose_action(game, difficulty))


def add_recommendation_if_needed() -> None:
    """Give the losing human a useful, free reading/listening suggestion."""
    global recommendation
    # In computer mode, Red is the human and Blue is the computer. In local
    # mode both players are human, so either losing player receives a tip.
    if game.winner is not None and (mode == "local" or game.winner == 1):
        recommendation = choice(FREE_LEARNING_RESOURCES)


@app.get("/")
def home():
    """Serve the page; JavaScript fetches the game state separately."""
    return render_template("index.html")


@app.get("/api/state")
def state():
    """Let the browser read the current game."""
    return jsonify(response_state())


@app.post("/api/new")
def new_game():
    """Replace the current in-memory game with a fresh game."""
    global game, mode, difficulty, recommendation
    settings = request.get_json(silent=True) or {}
    mode = settings.get("mode", "computer")
    difficulty = int(settings.get("difficulty", 3))
    if mode not in {"computer", "local"} or difficulty not in range(1, 6):
        return jsonify({"error": "Invalid game settings."}), 400
    game = GameState()
    recommendation = None
    return jsonify(response_state())


@app.post("/api/action")
def action():
    """Validate one browser action and return the updated game state."""
    payload = request.get_json(silent=True) or {}
    try:
        if game.winner is not None:
            raise InvalidMove("Start a new game to continue.")
        if mode == "computer" and game.turn == 1:
            raise InvalidMove("The computer is thinking.")
        kind = payload.get("kind")
        if kind == "place":
            game.place(int(payload["destination"]))
        elif kind == "move":
            game.move(int(payload["source"]), int(payload["destination"]))
        elif kind == "remove":
            game.remove(int(payload["position"]))
        else:
            raise InvalidMove("Action must be place, move, or remove.")
    except (InvalidMove, KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error), "state": response_state()}), 400
    play_computer_turn()
    add_recommendation_if_needed()
    return jsonify(response_state())


if __name__ == "__main__":
    # debug=True reloads after code changes. Never use it on a public server.
    app.run(debug=True)
