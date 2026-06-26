import os

from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()


class TextToSpeech:

    def __init__(self):

        self.client = DeepgramClient(
            api_key=os.getenv("DEEPGRAM_API_KEY")
        )

    def synthesize(
        self,
        text: str,
        output_file: str = "response.mp3"
    ) -> str:

        audio = (
            self.client
            .speak
            .v1
            .audio
            .generate(
                text=text,
                model="aura-2-asteria-en",
                encoding="mp3"
            )
        )

        with open(output_file, "wb") as f:

            for chunk in audio:

                f.write(chunk)

        return output_file