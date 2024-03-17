import socket
import threading
import sys

def client_thread(conn, addr, clients, names):
    """Handles a new client thread: receiving messages and broadcasting them to other clients."""
    name = None
    try:
        # Attempt to receive the client's name
        name = conn.recv(1024).decode()
        names[conn] = name
    except Exception as e:
        print(f"Error receiving name from {addr}: {e}")
        conn.close()
        return

    # Associate the connection with the client's name
    print(f"{name} connected from {addr}")
    
    # Loop to handle receiving messages from the client
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                print(f"{name}: {message}")  # Log message to the server console
                broadcast(f"{name}: {message}", conn, clients, names)  # Broadcast message to other clients
            else:
                # No message indicates the client has disconnected
                raise Exception("Client disconnected")
        except Exception as e:
            print(f"Client {name} error: {e}")
            break
    remove(conn, clients, names)

def broadcast(message, connection, clients, names):
    """Broadcasts a message to all clients except the sender."""
    for client in clients:
        if client != connection:  # Ensure the sender does not receive their own message
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Broadcast error to {names.get(client, 'unknown')}: {e}")
                remove(client, clients, names)

def remove(connection, clients, names):
    """Removes a client from the server's list of clients and names."""
    if connection in clients:
        clients.remove(connection)
        if connection in names:
            left_client_name = names[connection]
            print(f"{left_client_name} has left the chat room.")
            broadcast(f"{left_client_name} has left the chat room.", connection, clients, names)
            del names[connection]
        connection.close()

def main():
    """Main function to start the server and accept client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = '127.0.0.1'
    port = 12345

    try:
        server.bind((ip_address, port))
        server.listen()
    except Exception as e:
        print(f"Failed to bind or listen to the server: {e}")
        sys.exit(1)  # Exit the application with an error code

    clients = []  # Initialize a list to hold all client connections
    names = {}  # Initialize a dictionary to hold the names of clients

    print("Server is running and listening...")

    try:
        while True:
            conn, addr = server.accept()
            clients.append(conn)
            print(f"{addr} connected to the server.")
            threading.Thread(target=client_thread, args=(conn, addr, clients, names)).start()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        # Close all client connections
        for client in clients:
            client.close()
        server.close()
        print("Server shutdown complete.")

if __name__ == "__main__":
    main()
