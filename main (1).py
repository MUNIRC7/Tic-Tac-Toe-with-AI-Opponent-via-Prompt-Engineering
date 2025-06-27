import tkinter as tk
from tkinter import messagebox

# ---------- AI Logic (Minimax) ----------
def check_winner(board, player):
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return combo
    return None

def is_full(board):
    return all(cell != " " for cell in board)

def minimax(board, is_max):
    if check_winner(board, "O"): return 1
    if check_winner(board, "X"): return -1
    if is_full(board): return 0

    if is_max:
        best = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best = max(score, best)
        return best
    else:
        best = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best = min(score, best)
        return best

def get_ai_move(board):
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ---------- Game UI ----------
class TicTacToeUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe - Beat the AI")
        master.geometry("850x700")  
        master.configure(bg="#121212")

        self.board = [" "] * 9
        self.buttons = []
        self.won = False

        self.status_label = tk.Label(
            master, text="Your Turn (X)", font=("Arial", 14),
            bg="#121212", fg="#AAAAAA"
        )
        self.status_label.pack(pady=10)

        self.frame = tk.Frame(master, bg="#121212")
        self.frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.frame, text=" ", font=("Arial", 28, "bold"),
                bg="#1E1E1E", fg="#FFFFFF", width=4, height=2,
                command=lambda i=i: self.player_move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.restart_btn = tk.Button(
            master, text="🔁 Restart Game", font=("Arial", 12, "bold"),
            bg="#00AAFF", fg="white", command=self.restart_game
        )
        self.restart_btn.pack(pady=15)
        self.restart_btn.pack_forget()

    def player_move(self, index):
        if self.board[index] == " " and not self.won:
            self.board[index] = "X"
            self.buttons[index]["text"] = "X"
            self.buttons[index]["fg"] = "#00FFAA"
            self.status_label.config(text="AI's Turn (O)")
            win = check_winner(self.board, "X")
            if win:
                self.end_game("🎉 You Win!", win, "#00FFAA")
                return
            elif is_full(self.board):
                self.end_game("😐 It's a draw.", None, "#AAAAAA")
                return
            self.master.after(500, self.ai_move)

    def ai_move(self):
        move = get_ai_move(self.board)
        if move is not None:
            self.board[move] = "O"
            self.buttons[move]["text"] = "O"
            self.buttons[move]["fg"] = "#FF5555"
        win = check_winner(self.board, "O")
        if win:
            self.end_game("💀 You lost. Try again.", win, "#FF5555")
        elif is_full(self.board):
            self.end_game("😐 It's a draw.", None, "#AAAAAA")
        else:
            self.status_label.config(text="Your Turn (X)")

    def end_game(self, message, win_combo, color):
        self.won = True
        self.status_label.config(text=message)
        if win_combo:
            for i in win_combo:
                self.buttons[i].config(bg=color)
        self.restart_btn.pack()

    def restart_game(self):
        self.board = [" "] * 9
        self.won = False
        self.status_label.config(text="Your Turn (X)")
        for btn in self.buttons:
            btn.config(text=" ", bg="#1E1E1E", fg="white")
        self.restart_btn.pack_forget()

# ---------- Launch Game ----------
root = tk.Tk()
app = TicTacToeUI(root)
root.mainloop()
