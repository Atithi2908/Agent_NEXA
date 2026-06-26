import os

from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()


class SpeechToText:

    def __init__(self):

        self.client = DeepgramClient(
            api_key=os.getenv("DEEPGRAM_API_KEY")
        )

    def transcribe(
        self,
        audio_path: str
    ) -> str:

        with open(audio_path, "rb") as f:
            audio = f.read()

        response = (
            self.client
            .listen
            .v1
            .media
            .transcribe_file(
                request=audio,
                model="nova-3",
                language="en",
                smart_format=True,
                punctuate=True
            )
        )

        transcript = (
            response.results
            .channels[0]
            .alternatives[0]
            .transcript
        )

        return transcript.strip()