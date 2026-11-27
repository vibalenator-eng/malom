# Multiple Agents — Húzós snapszer

A small browser game prototype built in this repository as a demonstration of a three-role agent workflow: architecture, implementation, and QA. The interface is in Hungarian and uses a 20-card Hungarian deck.

## Run it

Requires Python 3.10+ and no third-party packages.

```powershell
cd "Multiple Agents"
python server.py
```

Open <http://localhost:8000>. Choose **Játék a gép ellen**, **Két játékos, egy eszköz**, or **Szoba létrehozása**. For online play, share the six-character room code; the other player opens the same server address and joins with that code. The server binds to all local network interfaces, so another device on the same Wi-Fi can connect using the host computer's local IP address and port 8000. Public internet play requires deploying the server on a reachable host; this prototype does not include hosting, accounts, persistence, encryption, or matchmaking.

See [Architecture and User Manual](./ARCHITECTURE_AND_USER_MANUAL.md) for the full component breakdown, room flow, rule assumptions, and step-by-step play instructions.

## Architecture

- `rules.py` contains the game state, card legality, trick resolution, drawing, and scoring.
- `server.py` owns rooms, validates actions, keeps both hands private, and serves the UI/API.
- `static/` contains the browser interface. It only receives the requesting player's hand and legal card IDs.

The server is authoritative. Room data exists in memory and is lost when the process stops. Room codes are invitations; each seat also receives a random private token.

## Rules used in this prototype

Regional rules differ, so this demo chooses one consistent two-player húzós variant:

- The deck has Ász, Tízes, Király, Felső, Alsó in Piros, Tök, Zöld, and Makk. Card points are 11, 10, 4, 3, and 2; trick order is Ász, Tízes, Király, Felső, Alsó.
- Each player receives five cards. Nine cards form the face-down talon and one more is exposed as trump. While the talon is open, any card may be played. The trick winner leads and draws first; the other player draws second.
- Once the talon is gone or covered, follow suit and beat the lead card if possible; otherwise play trump if available.
- A same-suit Király + Felső can be announced when leading: 20 points, or 40 in trump. The meld is credited after its owner has won a trick.
- On lead, the trump Alsó may exchange with the exposed trump. The talon can be covered after the first trick while at least two face-down cards remain.
- The first player to 66 wins. If the open-talon game reaches the final trick without anyone reaching 66, the final trick wins the deal.

The UI cites the [Schnapsen.at Hungarian rules](https://schnapsen.at/hu/szabalyok) as a reference. Local house rules can differ, especially around covering the talon and declarations.
