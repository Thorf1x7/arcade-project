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
                
                if self.selected:
                    selected_col = chess.square_file(self.selected)
                    selected_row = chess.square_rank(self.selected)
                    if col == selected_col and row == selected_row:
                        arcade.draw_polygon_filled(points, (0, 0, 255, 100))
                        
                        for move in self.moves:
                            if move.from_square == self.selected:
                                to_col = chess.square_file(move.to_square)
                                to_row = chess.square_rank(move.to_square)
                                if col == to_col and row == to_row:
                                    center_x = col * square_size + square_size // 2
                                    center_y = row * square_size + square_size // 2
                                    arcade.draw_circle_filled(center_x, center_y, square_size // 4 + 2, (0, 255, 0, 150))
        
        if not self.board.is_checkmate() and self.board.is_check():
            king = self.board.king(self.board.turn)
            if king:
                col = chess.square_file(king)
                row = chess.square_rank(king)
                x = col * square_size
                y = row * square_size
                points = [
                    (x, y),
                    (x + square_size, y),
                    (x + square_size, y + square_size),
                    (x, y + square_size)
                ]
                arcade.draw_polygon_filled(points, (255, 0, 0, 105))
        
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
        
        turn = 'Белые' if self.board.turn else 'Черные'
        self.turn_text.text = f'Ход: {turn}'
        self.turn_text.draw()
        
        if not self.game_over:
            if self.board.is_check() and not self.board.is_checkmate():
                self.status_text.text = "шах"
                self.status_text.color = arcade.color.RED
                self.status_text.draw()
        
        if self.game_over:
            self.result_text.text = self.result
            self.result_text.draw()
            
            arcade.Text('Нажмите R для новой игры.',
                       self.width // 2 - 145,
                       self.height // 2 - 45,
                       arcade.color.WHITE, 20).draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            return
            
        square_size = min(self.width, self.height) // 8
        col = int(x // square_size)
        row = int(y // square_size)
        
        if 0 <= col < 8 and 0 <= row < 8:
            square_cell = chess.square(col, row)
            
            if self.selected is None:
                piece = self.board.piece_at(square_cell)
                if piece and piece.color == self.board.turn:
                    self.selected = square_cell
                    self.moves = [move for move in self.board.legal_moves if move.from_square == square_cell]
            else:
                move = None
                
                for legal_move in self.moves:
                    if legal_move.to_square == square_cell:
                        move = legal_move
                        break
                
                if move is None:
                    move = chess.Move(self.selected, square_cell)
                    
                    piece = self.board.piece_at(self.selected)
                    if piece and piece.piece_type == chess.PAWN:
                        if (self.board.turn and row == 7) or (not self.board.turn and row == 0):
                            move = chess.Move(self.selected, square_cell, promotion=chess.QUEEN)
                
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.check_game()
                
                self.selected = None
                self.moves = []
                
    def check_game(self):
        if self.board.is_checkmate():
            self.game_over = True
            winner = "Черные" if self.board.turn else "Белые"
            self.result = f'Мат. Победили {winner}!'
        elif self.board.is_stalemate():
            self.game_over = True
            self.result = 'Пат - ничья'
        elif self.board.is_insufficient_material():
            self.game_over = True
            self.result = 'Недостаточно материала - ничья'
        elif self.board.is_fifty_moves():
            self.game_over = True
            self.result = '50 ходов без взятия - ничья'
        elif self.board.is_repetition(count=3):
            self.game_over = True
            self.result = 'Троекратное повторение позиции - ничья'
                
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.setup()
        elif key == arcade.key.Z:
            if len(self.board.move_stack) > 0 and not self.game_over:
                self.board.pop()
                self.selected = None
                self.moves = []
        elif key == arcade.key.ESCAPE:
            self.selected = None
            self.moves = []

def main():
    game = ChessGame(screen + 10, screen + 10, 'Шахматы')
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
