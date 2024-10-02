import pyttsx3
from gtts import gTTS
import tempfile
import os
import numpy as np
import librosa
import soundfile as sf

class TTSEngine:
    def __init__(self, use_cloud=False):
        """
        Initializes the TTS Engine.
        :param use_cloud: Boolean to decide whether to use a cloud-based TTS (gTTS) or local engine (pyttsx3).
        """
        self.use_cloud = use_cloud
        self.local_engine = pyttsx3.init()  # Local TTS engine
        self.local_engine.setProperty('rate', 150)  # Set speech rate
        self.local_engine.setProperty('volume', 1.0)  # Set volume level
        self.default_pitch = 100

    def synthesize(self, text, pitch_shift=1.0, emotion="neutral"):
        """
        Synthesize speech with optional pitch modulation and emotional tone.
        :param text: The text to be synthesized into speech.
        :param pitch_shift: Float value to modulate pitch (adjusts voice tone).
        :param emotion: Desired emotional tone of the voice (neutral, happy, sad).
        :return: Path to the synthesized audio file.
        """
        if self.use_cloud:
            return self.cloud_tts(text, pitch_shift, emotion)
        else:
            return self.local_tts(text, pitch_shift, emotion)

    def local_tts(self, text, pitch_shift, emotion):
        """
        Local TTS synthesis using pyttsx3 with pitch and emotion adjustments.
        """
        self.adjust_emotion(emotion)
        adjusted_pitch = self.default_pitch * pitch_shift
        self.local_engine.setProperty('pitch', adjusted_pitch)
        self.local_engine.save_to_file(text, 'local_tts_output.wav')
        self.local_engine.runAndWait()
        return 'local_tts_output.wav'

    def cloud_tts(self, text, pitch_shift, emotion):
        """
        Cloud-based TTS synthesis using gTTS (Google Text-to-Speech).
        """
        try:
            tts = gTTS(text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
                tts.save(temp_audio_file.name)
                return self.apply_pitch_modulation(temp_audio_file.name, pitch_shift, emotion)
        except Exception as e:
            return f"Error in cloud TTS synthesis: {str(e)}"

    def apply_pitch_modulation(self, audio_file, pitch_shift, emotion):
        """
        Apply pitch modulation to a synthesized audio file.
        :param audio_file: Path to the audio file to be modified.
        :param pitch_shift: Float value for pitch modulation.
        :param emotion: Desired emotional tone.
        :return: Path to the modulated audio file.
        """
        try:
            audio, sr = librosa.load(audio_file, sr=None)
            pitched_audio = librosa.effects.pitch_shift(audio, sr, n_steps=np.log2(pitch_shift))
            modulated_audio_path = audio_file.replace('.mp3', f'_modulated_{emotion}.wav')
            sf.write(modulated_audio_path, pitched_audio, sr)
            os.remove(audio_file)
            return modulated_audio_path
        except Exception as e:
            return f"Error applying pitch modulation: {str(e)}"

    def adjust_emotion(self, emotion):
        """
        Adjust the TTS engine properties to reflect emotional tone.
        :param emotion: The desired emotion ('neutral', 'happy', 'sad').
        """
        if emotion == "happy":
            self.local_engine.setProperty('rate', 180)
            self.local_engine.setProperty('volume', 1.2)
        elif emotion == "sad":
            self.local_engine.setProperty('rate', 100)
            self.local_engine.setProperty('volume', 0.8)
        else:
            self.local_engine.setProperty('rate', 150)
            self.local_engine.setProperty('volume', 1.0)