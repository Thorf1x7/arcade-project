import arcade
import chess

screen = 640
square = screen // 8

pieces = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', "k": "♚"
}

class ChessGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        
    def setup(self):
        self.board = chess.Board()
        self.selected = None
        self.moves = []
        self.game_over = False
        self.result = None
        
        self.turn_text = arcade.Text('', 5, screen - 15, arcade.color.WHITE, 15)
        self.status_text = arcade.Text("", screen // 2 - 95, screen - 35, arcade.color.YELLOW, 18)
        self.result_text = arcade.Text('', screen // 2 - 145, screen // 2, arcade.color.RED, 32)
        
    def on_draw(self):
        self.clear()
        
        square_size = min(self.width, self.height) // 8
        
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = arcade.color.LIGHT_GRAY
                else:
                    color = arcade.color.DARK_GRAY
                
                x = col * square_size
                y = row * square_size
                
                points = [
                    (x, y), (x + square_size, y), (x + square_size, y + square_size), (x, y + square_size)]
                arcade.draw_polygon_filled(points, color)
        
        for square_cell in chess.SQUARES:
            piece = self.board.piece_at(square_cell)
            if piece:
                col = chess.square_file(square_cell)
                row = chess.square_rank(square_cell)
                x = col * square_size + square_size // 2
                y = row * square_size + square_size // 2 + 2
                
                text = pieces[piece.symbol()]
                color = arcade.color.BLACK if piece.color == chess.BLACK else arcade.color.WHITE
                
                arcade.Text(text, x, y, color, square_size // 2 - 2, 
                          anchor_x="center", anchor_y="center").draw()

def main():
    game = ChessGame(screen + 10, screen + 10, 'Шахматы')
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()