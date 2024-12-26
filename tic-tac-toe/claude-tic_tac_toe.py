from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple
import logging

class GameSymbol(str, Enum):
    X = 'X'
    O = 'O'
    EMPTY = '_'

@dataclass
class Player:
    """Represents a player in the game."""
    name: str
    symbol: GameSymbol

class GameStatus(Enum):
    """Possible states of the game."""
    IN_PROGRESS = "in_progress"
    WIN = "win"
    DRAW = "draw"

class InvalidMoveError(Exception):
    """Raised when an invalid move is attempted."""
    pass

class Board:
    """Represents the game board and handles board-related operations."""
    def __init__(self, size: int):
        if not isinstance(size, int) or size < 3:
            raise ValueError("Board size must be an integer >= 3")
        self.size = size
        self._grid: List[List[str]] = [[GameSymbol.EMPTY for _ in range(size)] for _ in range(size)]

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is within board boundaries."""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Check if the given cell is empty."""
        return self._grid[row][col] == GameSymbol.EMPTY

    def place_symbol(self, row: int, col: int, symbol: GameSymbol) -> None:
        """Place a symbol on the board at the given position."""
        if not self.is_valid_position(row, col):
            raise InvalidMoveError("Position is outside board boundaries")
        if not self.is_cell_empty(row, col):
            raise InvalidMoveError("Cell is already occupied")
        self._grid[row][col] = symbol

    def get_cell(self, row: int, col: int) -> str:
        """Get the symbol at the given position."""
        return self._grid[row][col]

    def __str__(self) -> str:
        """Return a string representation of the board."""
        rows = []
        for i in range(self.size):
            row = " | ".join(self._grid[i])
            rows.append(row)
            if i != self.size - 1:
                rows.append("---" * self.size)
        return "\n".join(rows)

class Game:
    """Main game logic handler."""
    def __init__(self, player1: Player, player2: Player, board_size: int = 3):
        self.board = Board(board_size)
        self.players = (player1, player2)
        self.current_player_idx = 0
        self.moves_made = 0
        self.status = GameStatus.IN_PROGRESS
        self.winner: Optional[Player] = None
        logging.info(f"Started new game: {player1.name} vs {player2.name}")

    @property
    def current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_idx]

    def make_move(self, row: int, col: int) -> None:
        """Execute a move and update game state."""
        try:
            self.board.place_symbol(row, col, self.current_player.symbol)
            self.moves_made += 1
            logging.info(f"Player {self.current_player.name} moved to ({row}, {col})")

            if self._check_win(row, col):
                self.status = GameStatus.WIN
                self.winner = self.current_player
            elif self.moves_made == self.board.size ** 2:
                self.status = GameStatus.DRAW
            else:
                self._switch_player()

        except InvalidMoveError as e:
            logging.warning(f"Invalid move attempted: {str(e)}")
            raise

    def _check_win(self, row: int, col: int) -> bool:
        """Check if the current move resulted in a win."""
        symbol = self.current_player.symbol
        size = self.board.size

        # Check row
        if all(self.board.get_cell(row, i) == symbol for i in range(size)):
            return True

        # Check column
        if all(self.board.get_cell(i, col) == symbol for i in range(size)):
            return True

        # Check diagonals
        if row == col and all(self.board.get_cell(i, i) == symbol for i in range(size)):
            return True
        
        if row + col == size - 1 and all(self.board.get_cell(i, size-1-i) == symbol for i in range(size)):
            return True

        return False

    def _switch_player(self) -> None:
        """Switch to the next player."""
        self.current_player_idx = (self.current_player_idx + 1) % 2

class GameController:
    """Controls game flow and user interaction."""
    @staticmethod
    def create_game() -> Game:
        """Create a new game with player input."""
        player1_name = input("Name of Player 1: ").strip()
        player2_name = input("Name of Player 2: ").strip()
        
        player1 = Player(player1_name, GameSymbol.X)
        player2 = Player(player2_name, GameSymbol.O)
        
        return Game(player1, player2)

    def play_game(self, game: Game) -> None:
        """Main game loop."""
        print("\nGame started! Current board:")
        print(game.board)

        while game.status == GameStatus.IN_PROGRESS:
            move = self._get_valid_move(game)
            try:
                game.make_move(*move)
                print(f"\nCurrent board:")
                print(game.board)
            except InvalidMoveError as e:
                print(f"Invalid move: {e}")
                continue

        self._display_game_result(game)

    def _get_valid_move(self, game: Game) -> Tuple[int, int]:
        """Get and validate player move input."""
        while True:
            try:
                move_input = input(
                    f"\n{game.current_player.name}'s turn ({game.current_player.symbol})\n"
                    f"Enter row and column (0-{game.board.size-1}) separated by space: "
                )
                row, col = map(int, move_input.split())
                return row, col
            except ValueError:
                print("Invalid input format. Please enter two numbers separated by space.")

    def _display_game_result(self, game: Game) -> None:
        """Display the final game result."""
        if game.status == GameStatus.WIN:
            print(f"\nCongratulations! {game.winner.name} wins!")
        else:
            print("\nGame ended in a draw!")

def main():
    """Main entry point of the game."""
    logging.basicConfig(level=logging.INFO)
    controller = GameController()
    game = controller.create_game()
    controller.play_game(game)

if __name__ == "__main__":
    main()
