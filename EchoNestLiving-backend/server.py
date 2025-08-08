from flask import Flask, render_template, request, jsonify, abort
from flask_socketio import SocketIO, emit
import time
import eventlet
import json
import websockets
import asyncio
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")  # Enable WebSockets
#async_mode="eventlet"
#eventlet.monkey_patch()

ws_clients = set() 

# admin_username = "Waleed Ahmad"
# admin_password = "password4109"

# valid_username = "admin"
# valid_password = "password"

# In-memory list to store users
users = [
    {"id": 1, "username": "Waleed Ahmad", "password": "waleed123", "role": "Admin"},
    {"id": 2, "username": "Ahmad", "password": "ahmad123", "role": "User"}
]


# Dummy device states (for simulation)
device_states = {
    'light': 'OFF',
    'fan': 'OFF',
    'door': 'CLOSED',
    'window': 'CLOSED',
    'door-lock': 'LOCKED',
    'window-lock': 'LOCKED',
    'security': 'DISABLED',
}

toggle_rules = {
    "door": {"blocked_by": "door-lock", "blocked_state": "LOCKED", "error": " The door is LOCKED. Unlock it first."},
    "door-lock": {"blocked_by": "door", "blocked_state": "OPEN", "error": " Cannot LOCK the door while it's OPEN. Close it first."},
    "window": {"blocked_by": "window-lock", "blocked_state": "LOCKED", "error": " The window is LOCKED. Unlock it first."},
    "window-lock": {"blocked_by": "window", "blocked_state": "OPEN", "error": " Cannot LOCK the window while it's OPEN. Close it first."}
}



# Route to serve the dashboard page
@app.route('/')
def user_index():
    return render_template('login.html')


@app.route('/admin')
def admin_index():
    return render_template('admin_login.html')


@socketio.on("connect")
def handle_connect():
    print("SocketClient is connected")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password :
        return jsonify(success=False, message="Username and password are required"),400

    # Find the user by username
    user = next((user for user in users if user['username'] == username), None)
    if not user:
        return jsonify(success=False, message="Invalid username or password."), 401

    # Verify the password
    if user['password'] != password:
        return jsonify(success=False, message="Invalid username or password."), 401
    
    return jsonify(success=True)
    

@app.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password :
        return jsonify(success=False, message="Username and password are required"),400

    # Find the user by username
    user = next((user for user in users if user['username'] == username), None)
    if not user:
        return jsonify(success=False, message="Invalid username or password."), 401

    # Verify the password
    if user['password'] != password:
        return jsonify(success=False, message="Invalid username or password."), 401
    
    if user['role'].lower() != "admin":
        return jsonify(success=False, message="Only Admin can access this page."), 401
    
    return jsonify(success=True)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/admin-main')
def admin_main():
    return render_template("manage_users.html")


# Helper function to generate a new user ID
def generate_id():
    return max(user['id'] for user in users) + 1 if users else 1

# Routes

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Get a single user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    abort(404, description="User not found")

# Add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data or not 'role' in data:
        abort(400, description="Invalid input")
    
    # Check if username already exists
    if any(user['username'] == data['username'] for user in users):
        abort(400, description="Username already exists")

    # Check if password and confirm password match
    if data.get('password') != data.get('confirm_password'):
        abort(400, description="Passwords do not match")

    new_user = {
        "id": generate_id(),
        "username": data['username'],
        "password": data['password'],
        "role": data['role']
    }
    users.append(new_user)
    return jsonify({"message": "User added successfully", "user": new_user}), 201

# Update a user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data or not 'role' in data:
        abort(400, description="Invalid input")
    
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        abort(404, description="User not found")

    # Check if username already exists (excluding the current user)
    if any(u['username'] == data['username'] and u['id'] != user_id for u in users):
        abort(400, description="Username already exists")

    # Check if password and confirm password match
    if data.get('password') != data.get('confirm_password'):
        abort(400, description="Passwords do not match")

    user['username'] = data['username']
    user['password'] = data['password']
    user['role'] = data['role']
    return jsonify({"message": "User updated successfully", "user": user})

# Delete a user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        abort(404, description="User not found")
    
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"message": "User deleted successfully"})

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


# SocketIO event: Listen for device toggle requests from the client
@socketio.on('toggle_device')
def handle_toggle_device(data):
    device = data['device']
    new_state = data["state"]

    #1. Check if the toggle is restricted by another device
    if device in toggle_rules:
        rule = toggle_rules[device]
        dependent_device = rule["blocked_by"]
        if device_states.get(dependent_device) == rule["blocked_state"]:
            emit("error", {"message": rule["error"]}, to=request.sid)
            return

    #2. Prevent All Toggles When Security is ENABLED
    if device != "security" and device_states["security"] == "ENABLED":
        emit("error", {"message": f"Security System is ENABLED! Disable it first."}, to=request.sid)
        return

    # Update stored state
    device_states[device] = new_state
    print(f"Device '{device}' changed to {new_state}")
    
    asyncio.run(send_event_to_esp({"device":device, "state": new_state}))
    # Emit the updated state to the frontend
    socketio.emit('device_state_update', {'device': device, 'state': new_state}, to=None)
    


@socketio.on("voice_command")
def handle_voice_command(data):
    device = data['device']
    new_state = data["state"]

    #1. Check if the toggle is restricted by another device
    if device in toggle_rules:
        rule = toggle_rules[device]
        dependent_device = rule["blocked_by"]
        if device_states.get(dependent_device) == rule["blocked_state"]:
            emit("error", {"message": rule["error"]}, to=request.sid)
            return

    #2. Prevent All Toggles When Security is ENABLED
    if device != "security" and device_states["security"] == "ENABLED":
        emit("error", {"message": f"Security System is ENABLED! Disable it first."}, to=request.sid)
        return

    # Update stored state
    device_states[device] = new_state
    print(f"Device '{device}' changed to {new_state}")
    
    asyncio.run(send_event_to_esp({"device":device, "state": new_state}))
    # Emit the updated state to the frontend
    socketio.emit('device_state_update', {'device': device, 'state': new_state}, to=None)

@socketio.on('esp_connect')
def handle_esp_connect(data):
    print(f"ESP32 Identified: {data}")





@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


async def send_event_to_esp(event_data):
    for client in ws_clients:
        try:
            await client.send(json.dumps(event_data))
        except Exception as e:
            print(f"Failed to send event to client: {e}")


async def websocket_handler(websocket):
    ws_clients.add(websocket)
    print("ESP32 Connected via Websocket!")
    try:
        async for message in websocket:
            print(f"received from ESP32 : {message}")
            for client in ws_clients:
                await client.send(f"Echo : {message}")
    except websockets.exceptions.ConnectionClosed:
        print("ESP32 Disconnected!")
    finally:
        ws_clients.remove(websocket)

    
async def start_websocket_server():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await asyncio.Future()


def run_servers():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    flask_thread = Thread(target= lambda: socketio.run(app, host="0.0.0.0", port=8080))
    flask_thread.start()
    print("Flask server is starting...")

    loop.run_until_complete(start_websocket_server())

if __name__ == "__main__":
    run_servers()
