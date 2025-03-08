class Connect4:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 13)

    def make_move(self, column):
        if column < 0 or column >= 7 or self.board[0][column] != ' ':
            return False
        for row in reversed(self.board):
            if row[column] == ' ':
                row[column] = self.current_player
                break
        return True

    def check_winner(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == ' ':
                    continue
                if col + 3 < 7 and all(self.board[row][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]
                if row + 3 < 6 and all(self.board[row + i][col] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]
                if col + 3 < 7 and row + 3 < 6 and all(self.board[row + i][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]
                if col - 3 >= 0 and row + 3 < 6 and all(self.board[row + i][col - i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]
        return None

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play_game(self):
        while True:
            self.print_board()
            column = int(input(f"Player {self.current_player}, choose a column (0-6): "))
            if not self.make_move(column):
                print("Invalid move. Try again.")
                continue
            winner = self.check_winner()
            if winner:
                self.print_board()
                print(f"Player {winner} wins!")
                break
            self.switch_player()

if __name__ == "__main__":
    game = Connect4()
    game.play_game()
