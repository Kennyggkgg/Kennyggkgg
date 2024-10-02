import sys
import os
import ella  # Importing Ella's core functionalities
import hack  # Importing Hack's core functionalities
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from config import settings
from core.voice_interface import VoiceInterface

def main():
    # Initialize Ella and Hack
    ella_instance = ella.Ella()
    hack_instance = hack.Hack()
    
    # Retrieve voice settings
    voice_language = settings.VOICE_SETTINGS['language']
    voice_gender = settings.VOICE_SETTINGS['gender']
    
    # Initialize the voice interface
    voice_interface = VoiceInterface(voice_language, voice_gender)
    voice_interface.speak("Hello, I'm Ella, your personal assistant. How can I assist you today?")
    
    # Run Hack monitoring on a separate thread
    monitoring_thread = threading.Thread(target=hack_instance.silent_monitor)
    monitoring_thread.start()

    # Main loop
    while True:
        user_input = voice_interface.listen()  # Fixed here to use the correct instance
        
        if not isinstance(user_input, str) or user_input.strip() == "":
            voice_interface.speak("Sorry, I didn't catch that. Could you please repeat?")
            continue
        
        # Engage Ella's conversation
        ella_response = ella_instance.conversational_module.engage(user_input)
        voice_interface.speak(ella_response)
        
        # Handle dynamic learning and command execution
        ella_instance.handle_learning_and_commands(user_input)
        
        # Start or stop camera monitoring based on user input
        if "start camera" in user_input.lower():
            ella_instance.start_camera_monitoring()
        elif "stop camera" in user_input.lower():  # Fixed 'lif' typo
            ella_instance.stop_camera_monitoring()
        
        # Manage FM signals based on commands
        if "start FM" in user_input.lower():
            hack_instance.start_fm_communication()
        elif "stop FM" in user_input.lower():
            hack_instance.stop_fm_communication()
        
        # Handle singing command
        if "sing a song" in user_input.lower():
            ella_instance.sing_song_from_sd()

if __name__ == "__main__":
    main()