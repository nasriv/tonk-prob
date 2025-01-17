from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap
import sys
from tunk.game import Game

class CardWidget(QLabel):
    def __init__(self, card, parent=None):
        super().__init__(parent)
        self.card = card
        self.setText(f"{card[0]}{card[1]}")
        self.setStyleSheet("""
            QLabel {
                border: 1px solid black;
                background-color: white;
                padding: 5px;
                margin: 2px;
                min-width: 30px;
                min-height: 45px;
            }
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(f"{self.card[0]}{self.card[1]}")
            drag.setMimeData(mime)
            drag.exec()

class CardDropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QHBoxLayout(self)
        self.cards = []

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        card_text = event.mimeData().text()
        self.add_card(card_text)
        event.accept()

    def add_card(self, card_text):
        card_widget = CardWidget((card_text[0], card_text[1]), self)
        self.layout.addWidget(card_widget)
        self.cards.append(card_widget)

class TunkGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Tunk Game')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Player hand area
        self.player_hand = CardDropArea()
        main_layout.addWidget(QLabel("Your Hand:"))
        main_layout.addWidget(self.player_hand)

        # Spread area
        self.spread_area = CardDropArea()
        main_layout.addWidget(QLabel("Spreads:"))
        main_layout.addWidget(self.spread_area)

        # Discard pile
        self.discard_pile = CardDropArea()
        main_layout.addWidget(QLabel("Discard Pile:"))
        main_layout.addWidget(self.discard_pile)

        # Control buttons
        button_layout = QHBoxLayout()
        actions = ['Draw', 'Spread', 'Knock', 'Drop']
        for action in actions:
            btn = QPushButton(action)
            btn.clicked.connect(lambda checked, a=action: self.handle_action(a))
            button_layout.addWidget(btn)
        main_layout.addLayout(button_layout)

    def handle_action(self, action):
        if action == 'Draw':
            # Implement draw logic
            pass
        elif action == 'Spread':
            # Implement spread logic
            pass
        elif action == 'Knock':
            # Implement knock logic
            pass
        elif action == 'Drop':
            # Implement drop logic
            pass

def main():
    app = QApplication(sys.argv)
    gui = TunkGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
