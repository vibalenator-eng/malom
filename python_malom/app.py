"""Tkinter user interface for the Malom game.

Run with:  python -m python_malom.app
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .ai import choose_capture, choose_move
from .game import BLUE, Game, PLAYER_NAMES, RED, MILLS


POINTS = (
    (60, 60), (300, 60), (540, 60), (115, 115), (300, 115), (485, 115),
    (170, 170), (300, 170), (430, 170), (60, 300), (115, 300), (170, 300),
    (430, 300), (485, 300), (540, 300), (170, 430), (300, 430), (430, 430),
    (115, 485), (300, 485), (485, 485), (60, 540), (300, 540), (540, 540),
)
COLOUR = {RED: "#c85050", BLUE: "#316b88"}


class MalomApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Malom — Python edition")
        self.resizable(False, False)
        self.game = Game()
        self.selected: int | None = None
        self.computer_mode = tk.BooleanVar(value=True)
        self.level = tk.IntVar(value=3)
        self.status = tk.StringVar()
        self._build_ui()
        self.draw()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self, padding=16)
        outer.grid()
        controls = ttk.Frame(outer)
        controls.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ttk.Checkbutton(controls, text="Play against computer", variable=self.computer_mode, command=self.new_game).grid(row=0, column=0)
        ttk.Label(controls, text="Difficulty:").grid(row=0, column=1, padx=(20, 4))
        ttk.Combobox(controls, textvariable=self.level, values=(1, 2, 3, 4, 5), width=3, state="readonly").grid(row=0, column=2)
        ttk.Button(controls, text="New game", command=self.new_game).grid(row=0, column=3, padx=(20, 0))

        self.canvas = tk.Canvas(outer, width=600, height=600, background="#f7f1df", highlightthickness=0)
        self.canvas.grid(row=1, column=0)
        self.canvas.bind("<Button-1>", self.click_board)
        side = ttk.Frame(outer, padding=(18, 0, 0, 0))
        side.grid(row=1, column=1, sticky="n")
        ttk.Label(side, textvariable=self.status, wraplength=220, font=("Segoe UI", 11, "bold")).grid(sticky="w", pady=(0, 20))
        self.red_label = ttk.Label(side)
        self.red_label.grid(sticky="w", pady=5)
        self.blue_label = ttk.Label(side)
        self.blue_label.grid(sticky="w", pady=5)
        ttk.Separator(side).grid(sticky="ew", pady=16)
        ttk.Label(side, text="How to play", font=("Segoe UI", 10, "bold")).grid(sticky="w")
        ttk.Label(side, text="Click an empty point to place a piece.\nAfter placement, click your piece and then its destination.\nWith 3 pieces you may fly anywhere.", wraplength=220).grid(sticky="w", pady=(4, 0))

    def new_game(self) -> None:
        self.game.reset()
        self.selected = None
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")
        for line in MILLS:
            x1, y1 = POINTS[line[0]]
            x2, y2 = POINTS[line[2]]
            self.canvas.create_line(x1, y1, x2, y2, fill="#18232b", width=3)
        targets = set(self.game.legal_targets(self.selected)) if self.selected is not None else set()
        captures = set(self.game.captures()) if self.game.removal_required else set()
        for index, (x, y) in enumerate(POINTS):
            piece = self.game.board[index]
            if piece is None:
                fill = "#b98645" if index in targets else "#f7f1df"
                self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=fill, outline="#18232b", width=1)
            else:
                outline = "#b98645" if index in captures else "#18232b"
                width = 5 if index in captures or index == self.selected else 2
                self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill=COLOUR[piece], outline=outline, width=width)
        self.red_label.config(text=f"Red: {self.game.total_count(RED)} pieces ({self.game.reserve[RED]} to place)")
        self.blue_label.config(text=f"Blue: {self.game.total_count(BLUE)} pieces ({self.game.reserve[BLUE]} to place)")
        if self.game.finished:
            self.status.set("Draw!" if self.game.draw else f"{PLAYER_NAMES[self.game.winner]} wins!")
        elif self.game.removal_required:
            self.status.set(f"{PLAYER_NAMES[self.game.turn]} made a mill — remove a highlighted piece.")
        elif self.game.reserve[self.game.turn]:
            self.status.set(f"{PLAYER_NAMES[self.game.turn]}'s turn: place a piece.")
        else:
            self.status.set(f"{PLAYER_NAMES[self.game.turn]}'s turn: choose a piece, then a destination.")

    def point_at(self, event: tk.Event) -> int | None:
        return next((i for i, (x, y) in enumerate(POINTS) if (event.x - x) ** 2 + (event.y - y) ** 2 < 28 ** 2), None)

    def click_board(self, event: tk.Event) -> None:
        if self.game.finished or (self.computer_mode.get() and self.game.turn == BLUE):
            return
        point = self.point_at(event)
        if point is None:
            return
        if self.game.removal_required:
            self.game.capture(point)
        elif self.game.reserve[self.game.turn]:
            self.game.play(None, point)
        elif self.selected is None and self.game.board[point] == self.game.turn:
            self.selected = point
        elif self.selected is not None and self.game.play(self.selected, point):
            self.selected = None
        elif self.game.board[point] == self.game.turn:
            self.selected = point
        self.draw()
        if self.computer_mode.get() and self.game.turn == BLUE and not self.game.finished:
            self.after(350, self.computer_turn)

    def computer_turn(self) -> None:
        if self.game.finished or self.game.turn != BLUE:
            return
        source, target = choose_move(self.game, self.level.get())
        self.game.play(source, target)
        if self.game.removal_required:
            self.game.capture(choose_capture(self.game))
        self.draw()
        if self.game.finished:
            messagebox.showinfo("Game over", self.status.get())


if __name__ == "__main__":
    MalomApp().mainloop()
