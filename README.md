# EchoNest Living

**EchoNest Living** is a smart home automation system powered by **ESP32**, **Flask**, **WebSocket**, and **voice control**.  
It allows real-time appliance control through a **web dashboard**, **voice commands**, and hardware buttons — enabling seamless integration between IoT devices and the user.

---

## 🚀 Features

- **Real-time Device Control** via WebSocket (instant state updates)
- **Voice Command Processing** using Google Speech Recognition
- **Responsive Web Dashboard** for controlling appliances from any device
- **Authentication System** for secure access
- **ESP32-based Device Control** (lights, fans, doors, windows, etc.)
- **Multi-protocol Communication**:
  - HTTP for web control
  - WebSocket for real-time updates
  - TCP/IP for Python voice agent integration
- **Dynamic Device States** (ON/OFF, OPEN/CLOSED, LOCKED/UNLOCKED)
- **Hardware Integration** with relay modules and LEDs
- **Cross-device Compatibility** (PC, mobile, ESP32, Raspberry Pi-ready)

---

## 🛠️ Tech Stack

**Hardware:**
- ESP32 (38-pin NodeMCU)
- Relay Modules (4-channel)
- Jumper Wires & LEDs

**Backend:**
- Python 3 + Flask
- Flask-SocketIO
- Eventlet
- SpeechRecognition (Google API)
- SocketIO Python Client

**Frontend:**
- HTML, CSS, JavaScript
- WebSocket Client

**Protocols:**
- HTTP
- WebSocket
- TCP/IP

---

## 📡 System Architecture

1. **ESP32** receives device control commands from the Flask server via WebSocket.
2. **Flask Server** processes requests from the web dashboard and Python voice agent.
3. **Voice Agent** listens for commands, converts speech to text, and sends it to the server.
4. **Real-time Updates** are sent back to all connected clients to sync device states.

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/CodeWithWaleed-611/EchoNest-Living.git
cd EchoNest-Living
2️⃣ Install Backend Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Flash ESP32
Open ESP32_Firmware in Arduino IDE

Install ArduinoWebsockets and WiFi libraries

Flash code to ESP32 with correct Wi-Fi credentials

4️⃣ Run Flask Server
bash
Copy
Edit
python server.py
5️⃣ Access Web Dashboard
Open browser and go to:
http://<YOUR_PC_IP>:8080

🎤 Voice Agent Setup
bash
Copy
Edit
cd voice_agent
pip install -r requirements.txt
python voice_agent.py
Speak commands like:

"Turn on the light"

"Open the door"

"Disable the security system"


🧑‍💻 Author
Waleed Ahmad

GitHub: CodeWithWaleed-611

LinkedIn: (https://www.linkedin.com/in/waleed-ahmad-071b6b1a7)
