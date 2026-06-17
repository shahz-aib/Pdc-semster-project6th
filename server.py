import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

clients = []
usernames = []  # Store usernames separately

def broadcast(message, sender_client=None):
    """Send message to all clients"""
    for client in clients:
        try:
            # Don't send back to sender if specified
            if sender_client and client == sender_client:
                continue
            client.send(message.encode() if isinstance(message, str) else message)
        except:
            if client in clients:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            
            print(f"📨 Received: {message}")
            # Broadcast the message to everyone (including sender's client already shows it)
            broadcast(message, client)
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    # Clean up disconnected client
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        username = usernames.pop(index)
        broadcast(f"🔴 {username} left the chat")
        print(f"❌ {username} disconnected")
    client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"🟢 ParaChat Server running on {HOST}:{PORT}")
    print("Waiting for connections...\n")
    
    while True:
        client, addr = server.accept()
        print(f"🟡 New connection from: {addr}")
        
        # Request username
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()
        
        # Store client and username
        clients.append(client)
        usernames.append(username)
        
        print(f"📝 Username: {username}")
        
        # Notify everyone about new user
        broadcast(f"🟢 {username} joined the chat!")
        
        # Start thread for this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()
        
        print(f"📊 Active users: {len(clients)}\n")

if __name__ == "__main__":
    start_server()