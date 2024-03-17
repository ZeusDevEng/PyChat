import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QDialog,
                             QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QTextCursor, QPalette, QColor, QPixmap, QBrush

class ChatWindow(QWidget):
    def __init__(self, client, name):
        super().__init__()
        self.client = client
        self.name = name
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyChat – Connect, Share, and Enjoy')
        self.setGeometry(262, 201, 755, 492)

        # Set the background image
        palette = QPalette()
        bg_image = QPixmap('Assets/blue.jpeg').scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_image))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.chatLabel = QLabel("Chat Room")
        self.chatLabel.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.layout.addWidget(self.chatLabel)

        self.chatText = QTextEdit()
        self.chatText.setReadOnly(True)
        self.chatText.setStyleSheet("""
            QTextEdit {
                background-color: #fffbf2;
                border: 2px solid #D3D3D3;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
            }
        """)
        self.layout.addWidget(self.chatText)

        self.messageText = QLineEdit(self)
        self.messageText.setPlaceholderText("Type your message here...")
        self.messageText.setStyleSheet("""
            QLineEdit {
                border: 5px solid #fff2d8;
                border-radius: 20px;
                padding: 5px 15px;
                font-size: 14px;
                margin-bottom: 10px;
                color: #333333;
                background-color: #ffdfc3;
            }
        """)
        self.layout.addWidget(self.messageText)

        self.sendButton = QPushButton("Send")
        self.sendButton.setIcon(QIcon('Assets/send_icon.png'))
        self.sendButton.setStyleSheet("""
            QPushButton {
                background-color: #ffc088;
                color: white;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
                icon-size: 24px;
            }
            QPushButton:hover {
                background-color: #00BFFF;
            }
        """)
        self.layout.addWidget(self.sendButton)

        self.setLayout(self.layout)

        # Connect signals
        self.sendButton.clicked.connect(self.send_message)
        self.messageText.returnPressed.connect(self.send_message)

    def send_message(self):
        message = self.messageText.text().strip()
        if message:
            self.display_message(f"You: {message}")
            self.client.send(message.encode())
            self.messageText.clear()

    def display_message(self, message):
        self.chatText.append(message)
        self.chatText.moveCursor(QTextCursor.MoveOperation.End)

class UserNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyChat – Welcome')
        self.setGeometry(262, 201, 755, 492)

        # Set the background image
        palette = QPalette()
        bg_image = QPixmap('Assets/blue.jpeg').scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_image))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(QFont('Segoe UI', 16))
        self.lineEdit.setStyleSheet("""
            QLineEdit {
               background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
               stop:0 rgba(255, 242, 216, 210), stop:1 rgba(229, 229, 229, 255));
               color: #333333;
               border: 2px solid #ffc088;
               border-radius: 20px;
               padding: 15px;
            }
        """)
        self.lineEdit.setFixedHeight(60)
        self.lineEdit.setPlaceholderText("Enter your name")
        layout.addWidget(self.lineEdit)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(5, 5)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(255, 192, 136, 200))
        self.lineEdit.setGraphicsEffect(shadow_effect)

        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(40)

        self.okButton = QPushButton()
        okIcon = QIcon(QPixmap('Assets/check_icon.png').scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.okButton.setIcon(okIcon)
        self.okButton.setIconSize(QSize(30, 30))  
        self.okButton.setStyleSheet("""
            QPushButton {
                background-color: #32CD32;
                color: #FFFFFF;
                border-radius: 20px;
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #2E8B2E;
            }
        """)
        self.okButton.setFixedHeight(50)  
        buttonLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton()
        cancelIcon = QIcon(QPixmap('Assets/cross_icon.png').scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.cancelButton.setIcon(cancelIcon)
        self.cancelButton.setIconSize(QSize(30, 30))  
        self.cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: #FFFFFF;
                border-radius: 20px;
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
        """)
        self.cancelButton.setFixedHeight(50)  
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        # Connect signals
        self.okButton.clicked.connect(self.accept)
        self.lineEdit.returnPressed.connect(self.accept)

    def getUserName(self):
        return self.lineEdit.text().strip()
