import speech_recognition as sr
import wave
from voiceit2 import VoiceIt2

def record_voice(filename, duration=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording...")
        audio = recognizer.record(source, duration=duration)

    # save audio to the WAV file
    with wave.open(filename, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(audio.sample_rate)
        file.writeframes(audio.frame_data)
        print(f"Recording saved as {filename}")

record_voice('user_voice_data/user_voice_sample.wav')

vi = VoiceIt2("My API Key")
response = vi.create_user()
userId = response["userId"]

print(f"User created with ID: {userId}")

response = vi.create_enrollment(userId, 'en-US', 'user_voice_data/user_voice_sample.wav', 'your_phrase')
print(f"Enrollment response : {response}")

