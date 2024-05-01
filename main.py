import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=5,
                                   command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_click(self, i, j):
        if self.board[i*3 + j] == "" and not self.check_winner() and self.current_player == "X":
            self.buttons[i][j].config(text=self.current_player)
            self.board[i*3 + j] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} победил!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset_game()
            else:
                self.current_player = "O"
                self.ai_move()  

    def ai_move(self):
        score, move = self.minimax(self.board, self.current_player)
        if move is not None:
            self.buttons[move // 3][move % 3].config(text=self.current_player)
            self.board[move] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} победил!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset_game()
            else:
                self.current_player = "X"

    def minimax(self, board, player):
        avail_spots = [i for i, spot in enumerate(board) if spot == ""]

        if self.check_winner(board, "X"):
            return -10, None
        elif self.check_winner(board, "O"):
            return 10, None
        elif len(avail_spots) == 0:
            return 0, None

        best_score = -float('inf') if player == "O" else float('inf')
        best_move = None

        for move in avail_spots:
            new_board = board[:]
            new_board[move] = player
            score, _ = self.minimax(new_board, "O" if player == "X" else "X")
            if player == "O":
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def check_winner(self, board=None, player=None):
        if board is None:
            board = self.board
        if player is None:
            player = self.current_player

        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for line in lines:
            if all(board[i] == player for i in line):
                return True
        return False

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
                self.board[i*3 + j] = ""
        self.current_player = "X"

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()