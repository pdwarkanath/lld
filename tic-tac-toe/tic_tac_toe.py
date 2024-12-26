class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

class Board:
    def __init__(self, board_size: int):
        return [['_' for _ in range(board_size)] for _ in range(board_size)]

class Game:
    def __init__(self, player1: Player, player2: Player, board_size:int = 3):
        self.filled = 0
        self.is_over = False
        self.players = [player1, player2]
        self.board_size = board_size
        self.board = [['_' for _ in range(board_size)] for _ in range(board_size)]
        self.winner = None
    
    def draw_board(self):
        for i in range(self.board_size):
            print(" | ".join(self.board[i]))
            if i != self.board_size - 1:
                print("---"*self.board_size)

    def is_valid_move(self, row, col):
        return row >= 0 and row < self.board_size and col >= 0 and col < self.board_size and self.board[row][col] == '_'
    
    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
        self.filled += 1

    def has_player_won(self, row, col, player):
        rc, cc, dc1, dc2 = 0, 0, 0, 0
        # check row
        for sym in self.board[row]:
            if sym != player.symbol:
                break
            else:
                rc += 1
        # check column
        for i in range(self.board_size):
            sym = self.board[i][col]
            if sym != player.symbol:
                break
            else:
                cc += 1
        # check diagonal
        if row + col == self.board_size - 1:
            for i in range(self.board_size):
                if self.board[i][self.board_size - 1 - i] != player.symbol:
                    dc1 += 1
        
        if row == col:
            for i in range(self.board_size):
                if self.board[i][i] != player.symbol:
                    dc2 += 1

        if rc == self.board_size or cc == self.board_size or dc1 == self.board_size or dc2 == self.board_size:
            self.winner = player
            self.is_over = True
            return True
    
    def is_game_over(self):
        if self.filled == self.board_size * self.board_size:
            self.is_over = True
            return True
        
class GameController:
    def __init__(self):
        pass

    def create_game(self) -> Game:
        player1_name = input("Name of Player1: ")
        player1 = Player(player1_name, 'X')
        player2_name = input("Name of Player2: ")
        player2 = Player(player2_name, 'O')
        return Game(player1, player2)
    
    def play_game(self, game: Game):
        i = 0
        game.draw_board()
        while not game.is_over:
            i = i % 2
            curr_player = game.players[i]
            row, col = -1, -1
            first_time = True
            while not game.is_valid_move(row, col):
                if not first_time:
                    print(f"{row}, {col} is not a valid input. Try again")
                print(f"Enter row and column separated by space between 0 and {game.board_size-1} eg. 0 1")
                player_input = input(f"Where would you like to put {curr_player.symbol}? ")
                first_time = False
                try:
                    row, col = tuple(map(int, player_input.split()))
                except:
                    continue
            game.make_move(row, col, curr_player.symbol)
            game.draw_board()
            if game.has_player_won(row, col, curr_player):
                print(f"Congratulations, {game.winner.name}. You won!")
            elif game.is_game_over():
                print("It's a draw!")
            i += 1


gc = GameController()
game = gc.create_game()
gc.play_game(game)