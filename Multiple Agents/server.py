"""Small standard-library room server. Run with: python server.py"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import secrets
import threading
import urllib.parse

from rules import Game, CARD_POINTS, RANK_STRENGTH, SUITS

ROOT = Path(__file__).resolve().parent
ROOMS: dict[str, dict] = {}
LOCK = threading.RLock()


def ai_action(game: Game) -> None:
    """A simple legal, point-aware opponent that occasionally declares a marriage."""
    player = game.turn
    legal = game.legal_cards(player)
    # Prefer a legal card that wins a current trick; otherwise spend a low card.
    if game.lead_card:
        def takes(card):
            lead = game.lead_card
            return (card["suit"] == game.trump and lead["suit"] != game.trump) or (card["suit"] == lead["suit"] and RANK_STRENGTH[card["rank"]] > RANK_STRENGTH[lead["rank"]])
        winners = [c for c in legal if takes(c)]
        if winners:
            card = min(winners, key=lambda c: CARD_POINTS[c["rank"]])
        else:
            card = min(legal, key=lambda c: CARD_POINTS[c["rank"]])
    else:
        card = max(legal, key=lambda c: CARD_POINTS[c["rank"]])
    declare = next((s for s in SUITS if game.lead_card is None and s in {c["suit"] for c in game.hands[player] if c["rank"] == "K"} and s in {c["suit"] for c in game.hands[player] if c["rank"] == "F"}), None)
    if declare:
        card = next(c for c in legal if c["suit"] == declare and c["rank"] in {"K", "F"})
    game.play(player, card["id"], declare)


class Handler(BaseHTTPRequestHandler):
    server_version = "SnapszerDemo/1.0"

    def log_message(self, *_args):
        pass

    def _send(self, status: int, payload, content_type="application/json; charset=utf-8"):
        data = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(size) or b"{}")
        except (ValueError, json.JSONDecodeError):
            raise ValueError("Hibás kérés.")

    def _room(self, code):
        room = ROOMS.get(code.upper())
        if room is None:
            raise KeyError("Nem található ilyen szoba.")
        return room

    def _player(self, room, token):
        if room["mode"] == "hotseat" and token == room["tokens"][0]:
            return room["game"].turn
        try:
            return room["tokens"].index(token)
        except ValueError:
            raise PermissionError("Érvénytelen játékoskulcs.")

    def _view(self, room, player):
        if room["mode"] == "hotseat":
            player = room["game"].turn
        names = room["names"][:]
        if room["mode"] == "online" and not room["tokens"][1]:
            names[1] = "Várakozás..."
        return room["game"].view(player, "", room["code"], room["mode"], names)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            return self._send(200, (ROOT / "static" / "index.html").read_bytes(), "text/html; charset=utf-8")
        if parsed.path.startswith("/static/"):
            rel = parsed.path.removeprefix("/static/")
            if rel not in {"app.js", "style.css", "original-hungarian-tell-set.jpg"}:
                return self._send(404, {"error": "Nincs ilyen fájl."})
            p = ROOT / "static" / rel
            content_type = "image/jpeg" if rel.endswith(".jpg") else ("text/javascript; charset=utf-8" if rel.endswith(".js") else "text/css; charset=utf-8")
            return self._send(200, p.read_bytes(), content_type)
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "rooms"]:
            try:
                query = urllib.parse.parse_qs(parsed.query)
                with LOCK:
                    room = self._room(parts[2])
                    player = self._player(room, query.get("token", [""])[0])
                    self._send(200, self._view(room, player))
            except KeyError as exc:
                self._send(404, {"error": str(exc)})
            except PermissionError as exc:
                self._send(403, {"error": str(exc)})
            return
        self._send(404, {"error": "Nincs ilyen oldal."})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            body = self._body()
            if parsed.path == "/api/rooms":
                mode = body.get("mode", "ai")
                if mode not in {"ai", "online", "hotseat"}:
                    raise ValueError("Ismeretlen játékmód.")
                with LOCK:
                    code = secrets.token_urlsafe(4).replace("-", "").replace("_", "").upper()[:6]
                    while code in ROOMS:
                        code = secrets.token_urlsafe(4).replace("-", "").replace("_", "").upper()[:6]
                    token = secrets.token_urlsafe(24)
                    game = Game.new()
                    tokens = [token, None]
                    if mode == "ai":
                        tokens[1] = "AI"
                    elif mode == "hotseat":
                        tokens[1] = token
                    room = {"code": code, "mode": mode, "tokens": tokens, "names": [body.get("name") or "Piros", "Kék" if mode != "ai" else "Számítógép"], "game": game}
                    ROOMS[code] = room
                return self._send(201, {"code": code, "token": token, "player": 0})
            parts = parsed.path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "rooms"] and parts[3] == "join":
                with LOCK:
                    room = self._room(parts[2])
                    if room["mode"] != "online":
                        raise ValueError("Ehhez a szobához nem lehet csatlakozni.")
                    if room["tokens"][1]:
                        raise ValueError("A szoba már megtelt.")
                    token = secrets.token_urlsafe(24)
                    room["tokens"][1] = token
                    room["names"][1] = body.get("name") or "Kék"
                    return self._send(200, {"code": room["code"], "token": token, "player": 1})
            if len(parts) == 4 and parts[:2] == ["api", "rooms"] and parts[3] == "act":
                with LOCK:
                    room = self._room(parts[2])
                    player = self._player(room, body.get("token", ""))
                    game = room["game"]
                    recent_opponent_trick = None
                    if room["mode"] == "online" and room["tokens"][1] is None:
                        raise ValueError("Várjuk a másik játékost.")
                    action = body.get("action")
                    if action == "play":
                        game.play(player, body.get("card_id", ""), body.get("declare_suit"))
                        if game.last_trick_winner == 1 and len(game.last_trick or []) == 2:
                            recent_opponent_trick = game.last_trick[:]
                        if room["mode"] == "ai":
                            while not game.finished and game.turn == 1:
                                ai_action(game)
                                if game.last_trick_winner == 1 and len(game.last_trick or []) == 2:
                                    recent_opponent_trick = game.last_trick[:]
                    elif action == "close":
                        game.close_talon(player)
                    elif action == "exchange":
                        game.exchange_trump(player)
                    else:
                        raise ValueError("Ismeretlen lépés.")
                    view = self._view(room, player)
                    if recent_opponent_trick:
                        view["recent_opponent_trick"] = recent_opponent_trick
                    return self._send(200, view)
        except KeyError as exc:
            return self._send(404, {"error": str(exc)})
        except PermissionError as exc:
            return self._send(403, {"error": str(exc)})
        except ValueError as exc:
            return self._send(400, {"error": str(exc)})
        self._send(404, {"error": "Nincs ilyen útvonal."})


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    print(f"Snapszer fut: http://localhost:{port}")
    print("Másik eszköz a helyi hálózaton: http://<a gép IP-címe>:8000")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
