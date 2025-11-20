"""
Professional PyQt6 Chess Board Widget

A hardware-accelerated chess board widget using QGraphicsScene/QGraphicsView
with drag & drop support, animations, and modern pink/black color scheme.
"""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPen, QBrush, QPixmap, QPainter
import os


# Color scheme - Modern pink/black theme
LIGHT_SQUARE = QColor(255, 182, 193)  # Light pink
DARK_SQUARE = QColor(219, 112, 147)   # Pale violet red
HIGHLIGHT_COLOR = QColor(255, 255, 0, 120)  # Semi-transparent yellow
LEGAL_MOVE_COLOR = QColor(50, 205, 50, 100)  # Semi-transparent green
LAST_MOVE_COLOR = QColor(255, 165, 0, 100)  # Semi-transparent orange
SELECTED_COLOR = QColor(255, 215, 0, 150)  # Semi-transparent gold

# Board dimensions
SQUARE_SIZE = 70
BOARD_SIZE = 8
BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE


class ChessSquareItem(QGraphicsRectItem):
    """Individual chess square with highlighting capabilities"""

    def __init__(self, row, col, square_size=SQUARE_SIZE):
        super().__init__(0, 0, square_size, square_size)
        self.row = row
        self.col = col
        self.square_size = square_size
        self.original_color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
        self.highlight_color = None

        # Set initial appearance
        self.setBrush(QBrush(self.original_color))
        self.setPen(QPen(Qt.PenStyle.NoPen))

        # Position the square
        self.setPos(col * square_size, row * square_size)

    def set_highlight(self, color):
        """Set highlight color for this square"""
        self.highlight_color = color
        if color:
            self.setBrush(QBrush(color))
        else:
            self.setBrush(QBrush(self.original_color))

    def clear_highlight(self):
        """Remove highlight from this square"""
        self.set_highlight(None)


class ChessPieceItem(QGraphicsPixmapItem):
    """Draggable chess piece with smooth animations"""

    def __init__(self, piece, row, col, square_size=SQUARE_SIZE, parent=None):
        super().__init__(parent)
        self.piece = piece  # game.Piece object
        self.row = row
        self.col = col
        self.square_size = square_size
        self.scene_ref = None
        self.drag_start_pos = None
        self.original_pos = None

        # Load and scale piece image
        self.load_piece_image()

        # Enable dragging
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        # Enable smooth rendering
        self.setTransformationMode(Qt.TransformationMode.SmoothTransformation)

        # Position the piece
        self.update_position(row, col)

    def load_piece_image(self):
        """Load piece image from assets"""
        # Construct path to piece image
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                 'assets', 'images')
        image_path = os.path.join(base_path, self.piece.color, f"{self.piece.type}.png")

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Scale to fit square with some padding
            scaled_pixmap = pixmap.scaled(
                int(self.square_size * 0.85),
                int(self.square_size * 0.85),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)
        else:
            print(f"Warning: Could not load image at {image_path}")

    def update_position(self, row, col):
        """Update piece position on board"""
        self.row = row
        self.col = col
        # Center the piece in the square
        offset = (self.square_size - self.pixmap().width()) / 2
        self.setPos(col * self.square_size + offset, row * self.square_size + offset)

    def get_board_position(self):
        """Get current board position (row, col)"""
        return (self.row, self.col)

    def mousePressEvent(self, event):
        """Handle mouse press - start drag or selection"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.scenePos()
            self.original_pos = self.pos()
            if self.scene_ref:
                self.scene_ref.piece_pressed(self)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move - dragging"""
        if self.drag_start_pos:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release - complete move or return to original position"""
        if event.button() == Qt.MouseButton.LeftButton and self.drag_start_pos:
            # Get drop position in board coordinates
            drop_pos = event.scenePos()
            col = int(drop_pos.x() // self.square_size)
            row = int(drop_pos.y() // self.square_size)

            # Check if dropped on valid square
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if self.scene_ref:
                    self.scene_ref.piece_dropped(self, row, col)
            else:
                # Return to original position
                self.setPos(self.original_pos)

            self.drag_start_pos = None
        super().mouseReleaseEvent(event)


class ChessBoardScene(QGraphicsScene):
    """Chess board scene managing squares, pieces, and interactions"""

    # Signals
    moveAttempted = pyqtSignal(tuple, tuple)  # (from_pos, to_pos)
    squareClicked = pyqtSignal(tuple)  # (row, col)
    pieceSelected = pyqtSignal(tuple)  # (row, col)

    def __init__(self, parent=None):
        super().__init__(0, 0, BOARD_WIDTH, BOARD_WIDTH, parent)

        self.squares = []  # 2D array of ChessSquareItem
        self.pieces = {}  # Dict mapping (row, col) -> ChessPieceItem
        self.selected_piece = None
        self.legal_moves = []
        self.last_move = None  # (from_pos, to_pos)

        self.setup_board()

    def setup_board(self):
        """Initialize chess board squares"""
        self.squares = []
        for row in range(BOARD_SIZE):
            row_squares = []
            for col in range(BOARD_SIZE):
                square = ChessSquareItem(row, col)
                self.addItem(square)
                row_squares.append(square)
            self.squares.append(row_squares)

    def set_board_state(self, board):
        """Update board from game.Board object"""
        # Clear existing pieces
        for piece_item in self.pieces.values():
            self.removeItem(piece_item)
        self.pieces.clear()

        # Add pieces from board state
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.state[row][col]
                if piece:
                    piece_item = ChessPieceItem(piece, row, col)
                    piece_item.scene_ref = self
                    self.addItem(piece_item)
                    self.pieces[(row, col)] = piece_item

    def highlight_squares(self, positions, color):
        """Highlight specified squares with given color"""
        for row, col in positions:
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                self.squares[row][col].set_highlight(color)

    def clear_highlights(self):
        """Remove all highlights except last move"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.squares[row][col].clear_highlight()

        # Restore last move highlighting if exists
        if self.last_move:
            from_pos, to_pos = self.last_move
            self.squares[from_pos[0]][from_pos[1]].set_highlight(LAST_MOVE_COLOR)
            self.squares[to_pos[0]][to_pos[1]].set_highlight(LAST_MOVE_COLOR)

    def animate_move(self, from_pos, to_pos, duration_ms=300):
        """Animate piece movement from one square to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece_item = self.pieces.get(from_pos)
        if not piece_item:
            return

        # Calculate target position
        offset = (SQUARE_SIZE - piece_item.pixmap().width()) / 2
        target_x = to_col * SQUARE_SIZE + offset
        target_y = to_row * SQUARE_SIZE + offset

        # Create animation
        animation = QPropertyAnimation(piece_item, b"pos")
        animation.setDuration(duration_ms)
        animation.setStartValue(piece_item.pos())
        animation.setEndValue(QPointF(target_x, target_y))
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Update piece position after animation
        def on_animation_finished():
            piece_item.update_position(to_row, to_col)
            self.pieces[to_pos] = piece_item
            if from_pos in self.pieces:
                del self.pieces[from_pos]

        animation.finished.connect(on_animation_finished)
        animation.start()

        # Store animation reference to prevent garbage collection
        if not hasattr(self, '_animations'):
            self._animations = []
        self._animations.append(animation)

    def piece_pressed(self, piece_item):
        """Handle piece press event"""
        pos = piece_item.get_board_position()

        # If clicking the same piece, deselect it
        if self.selected_piece == piece_item:
            self.selected_piece = None
            self.clear_highlights()
            return

        # Select the piece
        self.selected_piece = piece_item
        self.clear_highlights()

        # Highlight selected square
        row, col = pos
        self.squares[row][col].set_highlight(SELECTED_COLOR)

        # Emit signal
        self.pieceSelected.emit(pos)

    def piece_dropped(self, piece_item, to_row, to_col):
        """Handle piece drop event"""
        from_pos = piece_item.get_board_position()
        to_pos = (to_row, to_col)

        # Check if this is a valid move (not the same square)
        if from_pos != to_pos:
            # Emit move attempted signal
            self.moveAttempted.emit(from_pos, to_pos)

        # Return piece to original position (will be updated by set_board_state if move is valid)
        piece_item.setPos(piece_item.original_pos)

    def mousePressEvent(self, event):
        """Handle mouse press on empty squares"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get clicked square
            pos = event.scenePos()
            col = int(pos.x() // SQUARE_SIZE)
            row = int(pos.y() // SQUARE_SIZE)

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                # Check if clicked on a piece
                item = self.itemAt(pos, self.views()[0].transform() if self.views() else None)
                if isinstance(item, ChessPieceItem):
                    # Let the piece handle it
                    pass
                else:
                    # Clicked on empty square
                    if self.selected_piece:
                        # Try to move selected piece to this square
                        from_pos = self.selected_piece.get_board_position()
                        to_pos = (row, col)
                        if from_pos != to_pos:
                            self.moveAttempted.emit(from_pos, to_pos)
                        self.selected_piece = None
                        self.clear_highlights()
                    else:
                        # Just emit square clicked
                        self.squareClicked.emit((row, col))

        super().mousePressEvent(event)

    def set_last_move(self, from_pos, to_pos):
        """Highlight the last move made"""
        self.last_move = (from_pos, to_pos)
        self.clear_highlights()

    def set_legal_moves(self, moves):
        """Highlight legal moves for selected piece"""
        self.legal_moves = moves
        self.highlight_squares(moves, LEGAL_MOVE_COLOR)


class ChessBoardWidget(QGraphicsView):
    """Main chess board widget with anti-aliasing and smooth rendering"""

    # Forward signals from scene
    moveAttempted = pyqtSignal(tuple, tuple)
    squareClicked = pyqtSignal(tuple)
    pieceSelected = pyqtSignal(tuple)

    def __init__(self, parent=None):
        self.board_scene = ChessBoardScene()
        super().__init__(self.board_scene, parent)

        # Connect scene signals to widget signals
        self.board_scene.moveAttempted.connect(self.moveAttempted.emit)
        self.board_scene.squareClicked.connect(self.squareClicked.emit)
        self.board_scene.pieceSelected.connect(self.pieceSelected.emit)

        # Configure view for optimal rendering
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        # Disable scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set fixed size
        self.setFixedSize(BOARD_WIDTH + 2, BOARD_WIDTH + 2)

        # Optional: Disable view transformations to ensure 1:1 pixel mapping
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

    def set_board_state(self, board):
        """Update board display from game.Board object"""
        self.board_scene.set_board_state(board)

    def highlight_squares(self, positions, color=LEGAL_MOVE_COLOR):
        """Highlight specified squares"""
        self.board_scene.highlight_squares(positions, color)

    def clear_highlights(self):
        """Clear all highlights"""
        self.board_scene.clear_highlights()

    def animate_move(self, from_pos, to_pos, duration_ms=300):
        """Animate piece movement"""
        self.board_scene.animate_move(from_pos, to_pos, duration_ms)

    def set_last_move(self, from_pos, to_pos):
        """Highlight the last move"""
        self.board_scene.set_last_move(from_pos, to_pos)

    def set_legal_moves(self, moves):
        """Highlight legal moves for selected piece"""
        self.board_scene.set_legal_moves(moves)
