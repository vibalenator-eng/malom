# Multiple Agents — Húzós snapszer

A small browser game prototype built in this repository as a demonstration of a three-role agent workflow: architecture, implementation, and QA. The interface is in Hungarian and uses a 20-card Hungarian deck.

## Run it

Requires Python 3.10+ and no third-party packages.

```powershell
cd "Multiple Agents"
python server.py
```

Open <http://localhost:8000>. Choose one of five computer difficulty levels, **Két játékos, egy eszköz**, or **Szoba létrehozása**. For online play, share the six-character room code; the other player opens the same server address and joins with that code. The server binds to all local network interfaces, so another device on the same Wi-Fi can connect using the host computer's local IP address and port 8000. Public internet play requires deploying the server on a reachable host; this prototype does not include hosting, accounts, encryption, or matchmaking. Active room state is in memory, while finished computer games are saved in a bounded local JSONL training archive.

See [Architecture and User Manual](./ARCHITECTURE_AND_USER_MANUAL.md) for the full component breakdown, room flow, rule assumptions, and step-by-step play instructions.

## Architecture

- `rules.py` contains the game state, card legality, trick resolution, drawing, and scoring.
- `ai.py` implements five computer levels: random legal play, a basic low-point heuristic, a point-aware strategy, and two hidden-card sampling levels.
- `training_data.py` saves completed human-versus-computer games as JSONL for future offline learning. It keeps the newest 1,000 games by default; set `SNAPSZER_MAX_TRAINING_GAMES=10000` before starting the server to retain up to 10,000.
- `server.py` owns rooms, validates actions, keeps both hands private, serves the HTTP/JSON API, and records completed computer games.
- `static/` contains the browser interface. It only receives the requesting player's hand and legal card IDs.

The server is authoritative. Active room data exists in memory and is lost when the process stops. Room codes are invitations; each seat also receives a random private token. Only completed computer games are kept between restarts, in `data/ai_training_games.jsonl`. The current archive snapshot is included in this repository at the user's request; future completed games update that tracked file. The sixth **Tanuló** level is not active yet: the stored games are training material, not automatic learning.

## Rules used in this prototype

Regional rules differ, so this demo chooses one consistent two-player húzós variant:

- The deck has Ász, Tízes, Király, Felső, Alsó in Piros, Tök, Zöld, and Makk. Card points are 11, 10, 4, 3, and 2; trick order is Ász, Tízes, Király, Felső, Alsó.
- Each player receives five cards. Nine cards form the face-down talon and one more is exposed as trump. While the talon is open, any card may be played. The trick winner leads and draws first; the other player draws second.
- Once the talon is gone or covered, follow suit and beat the lead card if possible; otherwise play trump if available.
- A same-suit Király + Felső can be announced when leading: 20 points, or 40 in trump. The meld is credited after its owner has won a trick.
- On lead, the trump Alsó may exchange with the exposed trump. The talon can be covered after the first trick while at least two face-down cards remain.
- The first player to 66 wins. If the open-talon game reaches the final trick without anyone reaching 66, the final trick wins the deal.

The UI cites the [Schnapsen.at Hungarian rules](https://schnapsen.at/hu/szabalyok) as a reference. Local house rules can differ, especially around covering the talon and declarations.
