import pyttsx3 as pts
import speech_recognition as sr
import websocket_client as ws_client
import sys
import time


engine = pts.init()

# Customizing voice agent properties
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


valid_commands = {
    "light":[
        {"device":"light", "state":"OFF"},
        {"device":"light", "state":"ON"}],
    "fan":[
        {"device":"fan", "state":"OFF"},
        {"device":"fan", "state":"ON"}],
    "door":[
        {"device":"door", "state":"CLOSED"},
        {"device":"door", "state":"OPEN"}],
    "window":[
        {"device":"window", "state":"CLOSED"},
        {"device":"window", "state":"OPEN"}],
    "window-lock":[
        {"device":"window-lock", "state":"UNLOCKED"},
        {"device":"window-lock", "state":"LOCKED"}],
    "door-lock":[
        {"device":"door-lock", "state":"UNLOCKED"},
        {"device":"door-lock", "state":"LOCKED"}],
    "security-system":[
        {"device":"security", "state":"DISABLED"},
        {"device":"security", "state":"ENABLED"}]
}
# To receive acknowledgements
def speak(text):
    engine.say(text) 
    engine.runAndWait()
    
# Extractng semantic from voice 
# Send command to the EchoNest Living server
def sendCmdToServer(text):
    if "light" in text and "on" in text:
        speak("Ok, Turnning ON the light")
        ws_client.send_command(valid_commands["light"][1])
    elif "light" in text and "off" in text:
        speak("ok, Turnning OFF the light.")
        ws_client.send_command(valid_commands["light"][0])
    elif "door" in text and "open" in text:
        speak("Ok, Openning the door.")
        ws_client.send_command(valid_commands["door"][1])
    elif "door" in text and "close" in text:
        speak("Ok, Clossing the door.")
        ws_client.send_command(valid_commands["door"][0])
    elif "fan" in text and "on" in text:
        speak("OK, Turnning ON the fan.")
        ws_client.send_command(valid_commands["fan"][1])
    elif "fan" in text and "off" in text:
        speak("OK, Turnning OFF the fan.")
        ws_client.send_command(valid_commands["fan"][0])
    elif "window" in text and "open" in text:
        speak("OK, Openning the window")
        ws_client.send_command(valid_commands["window"][1])
    elif "window" in text and "close" in text: 
        speak("OK, Closing the window")
        ws_client.send_command(valid_commands["window"][0])
    elif "door" in text and "unlock" in text:
        speak("Ok, door unlocking.")
        ws_client.send_command(valid_commands["door-lock"][0])
    elif "door" in text and "lock" in text:
        speak("Ok, door locking.")
        ws_client.send_command(valid_commands["door-lock"][1])
    elif "window" in text and "unlock" in text:
        speak("Ok, window unlocking.")
        ws_client.send_command(valid_commands["window-lock"][0])
    elif "window" in text and "lock" in text:
        speak("OK, window locking")
        ws_client.send_command(valid_commands["window-lock"][1])
    elif "security system" in text and "on" in text:
        speak("OK, Enabling the Security System.")
        ws_client.send_command(valid_commands["security-system"][1])
    elif "security system" in text and "off" in text:
        speak("OK, Disabling the Security System.")
        ws_client.send_command(valid_commands["security-system"][0])

# Greetings
speak("Hello Waleed!. My name is Robo, I am your voice assistant.")
r = sr.Recognizer()



#recognize voice with attached microphone
while True:
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("Listening...")
        audio = r.listen(source)
        text = None
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("The Speech Recognition could not understand audio")
        except sr.RequestError as e:
            speak(f"Could not request results from Speech Recognition server; {e}")
        except sr.SomeException as e:
            speak(f"Exception case : {e}")

        print(text)
        if type(text) == str:
            if "stop" in text and "program" in text:
                speak("OK, Stopped the execution")
                sys.exit()            
                ws_client.disconnect()
            elif "disconnect" in text and "server" in text:
                speak("OK, Disconnecting EchoNest Living.")
                ws_client.disconnect()
            elif "connect" in text and "server" in text:
                speak("OK, Connecting EchoNest Living.")
                ws_client.connect_to_EchoNest()
            else:
                sendCmdToServer(text)

        time.sleep(0.75)






            