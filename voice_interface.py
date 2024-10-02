import speech_recognition as sr
import pyttsx3

class VoiceInterface:
    def __init__(self, language='en', gender='male'):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.gender = gender
        self.engine = pyttsx3.init()
        
        voices = self.engine.getProperty('voices')
        if voices:
            # Safely setting voice based on gender, assuming at least two voices
            if gender == 'male' and len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
            elif gender == 'female' and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            else:
                print("Selected gender voice not found, using default voice.")
        else:
            print("No voices found on this system.")
        
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Optional: Adjust for background noise
            audio = self.recognizer.listen(source)
        try:
            user_input = self.recognizer.recognize_google(audio, language=self.language)
            print(f"User said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
    
    def speak(self, text):
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()