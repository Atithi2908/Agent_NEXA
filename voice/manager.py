import os

from voice.recorder import Recorder
from voice.stt import SpeechToText
from voice.tts import TextToSpeech
from voice.player import AudioPlayer


class VoiceManager:

    def __init__(self):

        self.recorder = Recorder()

        self.stt = SpeechToText()

        self.tts = TextToSpeech()

        self.player = AudioPlayer()

    def listen(self) -> str:

        audio_path = self.recorder.record()

        text = self.stt.transcribe(
            audio_path
        )

        if os.path.exists(audio_path):
            os.remove(audio_path)

        return text

    def speak(
        self,
        text: str
    ):

        audio_path = self.tts.synthesize(
            text
        )

        self.player.play(
            audio_path
        )

        if os.path.exists(audio_path):
            os.remove(audio_path)