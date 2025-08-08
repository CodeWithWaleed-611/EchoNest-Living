import socketio


# Create a socket object
client_socket_io = socketio.Client()


device_states = {
    'light': 'OFF',
    'fan': 'OFF',
    'door': 'CLOSED',
    'window': 'CLOSED',
    'door-lock': 'LOCKED',
    'window-lock': 'LOCKED',
    'security': 'DISABLED',
}

# Event: Connected successfully to Flask WebSocket
@client_socket_io.event
def connect():
    print("Successfully connected to EchoNest Living.")

# Event: Handle error messages from EchoNest Living

@client_socket_io.on("error")
def handle_error(data):
    message = data['message']
    print(f"Server response : {message}")  # Show error message in console
    

@client_socket_io.on("device_state_update")
def handle_device_update(data):
    device = data['device']
    state = data['state']
    print(f"{device} is now {state}.")
    

# Event: Connection failed
@client_socket_io.event
def connect_error(data):
    print(f"Connection failed! Error: {data}")

# Event: Disconnected from the server
@client_socket_io.event
def disconnect():
    print("Disconnected from EchoNest Living.")

# Connect to the ESP32 SoftAP
host = '192.168.123.51'  # ESP32 IP address
port = 8080  # Server port    
# Connect to Flask WebSocket Server
try:
    client_socket_io.connect(f"http://{host}:{port}")  # Change to your Flask server IP
except Exception as e:
    print(f"WebSocket connection failed: {e}")


def connect_to_EchoNest():
    try:
        client_socket_io.connect(f"http://{host}:{port}")  # Change to your Flask server IP
    except Exception as e:
        print(f"WebSocket connection failed: {e}")

def send_command(command):
    client_socket_io.emit("voice_command", command)  # Send to Flask

def disconnect():
    # Close the connection
    client_socket_io.disconnect()





