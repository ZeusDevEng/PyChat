import sys
import socket
import threading
from PyQt6.QtWidgets import QApplication, QDialog
from gui import ChatWindow, UserNameDialog

class Client:
    """A client for handling the connection and communication with the server."""
    
    def __init__(self):
        """Initializes the Client instance and sets up the client socket."""
        self.client = None
        self.setup_client()

    def setup_client(self):
        """Sets up the client socket connection to the server."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket for IPv4 and TCP
        ip_address = '127.0.0.1'  # Server IP address
        port = 12345  # Server port number
        try:
            self.client.connect((ip_address, port))  # Attempt to connect to the server
        except ConnectionError:
            print("Failed to connect to the server.")  # Connection failed
            sys.exit()  # Exit the application if connection to the server fails

    def send_message(self, message):
        """Sends a message to the server."""
        self.client.send(message.encode())  # Encode and send the message

    def receive_messages(self, chat_window):
        """Receives messages from the server and displays them in the chat window."""
        while True:
            try:
                message = self.client.recv(1024).decode()  # Receive and decode the message
                chat_window.display_message(message)  # Display the received message in the chat window
            except Exception as e:
                print(f"An error occurred: {e}")  # Print any exceptions that occur
                self.client.close()  # Close the client socket
                break  # Exit the loop

def main():
    """Main function to start the client application."""
    app = QApplication(sys.argv)  # Create a QApplication instance
    dialog = UserNameDialog()  # Create an instance of the UserNameDialog

    # Execute the dialog and check if the user accepted it
    if dialog.exec() == QDialog.DialogCode.Accepted:
        userName = dialog.getUserName()  # Retrieve the username from the dialog
        if userName:
            client = Client()  # Create a Client instance
            client.send_message(userName)  # Send the username to the server
            chatWindow = ChatWindow(client.client, userName)  # Create the chat window
            threading.Thread(target=client.receive_messages, args=(chatWindow,), daemon=True).start()  # Start receiving messages
            chatWindow.show()  # Show the chat window
            sys.exit(app.exec())  # Start the application's main loop

if __name__ == '__main__':
    main()
