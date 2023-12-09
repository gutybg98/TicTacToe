import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("TicTacToe")

        self.create_buttons()
        self.master.eval('tk::PlaceWindow . center')
        if not messagebox.askyesno('Start', 'Do you want to start?'):
            self.buttons[0].config(text='X', fg='red')
            self.bot_starts = True
        else:
            self.bot_starts = False

    def create_buttons(self):
        self.buttons = [self.create_button(
            row, column) for row in range(3) for column in range(3)]

    def create_button(self, row, column):
        button = tk.Button(self.master, text='', width=15, height=5)
        button.bind('<Button-1>', lambda event,
                    button=button: self.player_move(button))
        button.grid(row=row+1, column=column+1)
        return button

    def free_buttons(self):
        return [button for button in self.buttons if button.cget('text') == '']

    def check_game_over(self):
        victory = self.victory_for()
        if victory:
            if victory == 'X':
                messagebox.showinfo("Game Over", "Bot Wins!")
            elif victory == 'O':
                messagebox.showinfo("Game Over", "You win!")
            response = messagebox.askquestion(
                "Reset?", "Do you want to play again?")
            if response == 'yes':
                self.reset_game()
            else:
                self.master.quit()
        elif not self.free_buttons():
            messagebox.showinfo("Game Over", "It's a draw!")
            response = messagebox.askquestion(
                "Reset?", "Do you want to play again?")
            if response == 'yes':
                self.reset_game()
            else:
                self.master.quit()

    def victory_for(self):
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in winning_combinations:
            if self.buttons[combo[0]].cget('text') == self.buttons[combo[1]].cget('text') == self.buttons[combo[2]].cget('text') != '':
                return self.buttons[combo[0]].cget('text')
        return None

    def minimax(self, board, player):
        available_spots = self.free_buttons()

        if self.victory_for() == 'X':
            return {'score': 10}
        elif self.victory_for() == 'O':
            return {'score': -10}
        elif not available_spots:
            return {'score': 0}

        moves = []

        for spot in available_spots:
            move = {}
            move['index'] = self.buttons.index(spot)
            spot.config(text=player)

            if player == 'X':
                result = self.minimax(board, 'O')
                move['score'] = result['score']
            else:
                result = self.minimax(board, 'X')
                move['score'] = result['score']

            spot.config(text='')
            moves.append(move)

        best_move = None
        if player == 'X':
            best_score = -float('inf')
            for move in moves:
                if move['score'] > best_score:
                    best_score = move['score']
                    best_move = move
        else:
            best_score = float('inf')
            for move in moves:
                if move['score'] < best_score:
                    best_score = move['score']
                    best_move = move

        return best_move

    def whos_turn(self):
        count_symbol = [button.cget(
            'text') for button in self.buttons if button.cget('text') in ['X', 'O']]
        if self.bot_starts:
            self.player_turn = count_symbol.count(
                'X') > count_symbol.count('O')
        else:
            self.player_turn = count_symbol.count(
                'X') == count_symbol.count('O')

    def player_move(self, button):
        self.check_game_over()
        self.whos_turn()
        if self.player_turn and button in self.free_buttons():
            button.config(text='O', fg='green')
            self.check_game_over()
            self.master.after(100, self.bot_move)

    def bot_move(self):
        self.check_game_over()
        self.whos_turn()
        if not self.player_turn:
            move = self.minimax(self.buttons, 'X')['index']
            self.buttons[move].config(text='X', fg='red')
            self.check_game_over()

    def reset_game(self):
        self.create_buttons()
        self.master.eval('tk::PlaceWindow . center')
        if not messagebox.askyesno('Start', 'Do you want to start?'):
            self.buttons[0].config(text='X', fg='red')
            self.bot_starts = True
        else:
            self.bot_starts = False


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
