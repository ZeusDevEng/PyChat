import socket
import threading

def client_thread(conn, addr, clients, names):
    """Handles a new client thread: receiving messages and broadcasting them to other clients."""
    try:
        # Attempt to receive the client's name
        name = conn.recv(1024).decode()
    except Exception as e:
        print(f"Error receiving name: {e}")
        return

    # Associate the connection with the client's name
    names[conn] = name
    
    # Loop to handle receiving messages from the client
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                print(f"{name}: {message}")  # Log message to the server console
                broadcast(f"{name}: {message}", conn, clients, names)  # Broadcast message to other clients
            else:
                # No message indicates the client has disconnected
                remove(conn, clients, names)
                break
        except Exception as e:
            print(f"Error handling message: {e}")
            break

def broadcast(message, connection, clients, names):
    """Broadcasts a message to all clients except the sender."""
    for client in clients:
        if client != connection:  # Ensure the sender does not receive their own message
            try:
                client.send(message.encode())
            except:
                # Handle a failed send by removing the client
                remove(client, clients, names)

def remove(connection, clients, names):
    """Removes a client from the server's list of clients and names."""
    if connection in clients:
        clients.remove(connection)
        if connection in names:
            print(f"{names[connection]} has left the chat room.")  # Log departure to the server console
            del names[connection]

def main():
    """Main function to start the server and accept client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = '127.0.0.1'
    port = 12345
    server.bind((ip_address, port))  # Bind the server to the specified IP address and port
    server.listen()

    clients = []  # Initialize a list to hold all client connections
    names = {}  # Initialize a dictionary to hold the names of clients

    print("Server is running and listening...")

    # Start an infinite loop to continuously accept new connections
    while True:
        conn, addr = server.accept()  # Accept a new connection
        clients.append(conn)  # Add the new connection to the list of clients
        print(f"{addr} connected to the server.")  # Log new connection to the server console
        # Start a new thread for each client connection
        threading.Thread(target=client_thread, args=(conn, addr, clients, names)).start()

if __name__ == "__main__":
    main()
