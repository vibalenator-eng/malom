"""Flask web server for the Malom learning project."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from game_engine import GameState, InvalidMove

app = Flask(__name__)
game = GameState()  # Kept in memory: perfect for a local learning project.


@app.get("/")
def home():
    """Serve the page; JavaScript fetches the game state separately."""
    return render_template("index.html")


@app.get("/api/state")
def state():
    """Let the browser read the current game."""
    return jsonify(game.as_dict())


@app.post("/api/new")
def new_game():
    """Replace the current in-memory game with a fresh game."""
    global game
    game = GameState()
    return jsonify(game.as_dict())


@app.post("/api/action")
def action():
    """Validate one browser action and return the updated game state."""
    payload = request.get_json(silent=True) or {}
    try:
        if game.winner is not None:
            raise InvalidMove("Start a new game to continue.")
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
        return jsonify({"error": str(error), "state": game.as_dict()}), 400
    return jsonify(game.as_dict())


if __name__ == "__main__":
    # debug=True reloads after code changes. Never use it on a public server.
    app.run(debug=True)
