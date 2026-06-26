import os
import tempfile

import sounddevice as sd
from scipy.io.wavfile import write

from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

client = DeepgramClient(api_key=DEEPGRAM_API_KEY)


SAMPLE_RATE = 16000
DURATION = 5


def record_audio():

    print("\nListening...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    temp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    write(
        temp.name,
        SAMPLE_RATE,
        audio
    )

    return temp.name


def transcribe(path):

    with open(path, "rb") as f:

        payload = {
            "buffer": f,
        }

        response = (
            client.listen.rest.v("1").transcribe_file(
                payload,
                {
                    "model": "nova-3",
                    "smart_format": True,
                    "punctuate": True,
                },
            )
        )

    return (
        response.results.channels[0]
        .alternatives[0]
        .transcript
    )


def listen():

    audio = record_audio()

    text = transcribe(audio)

    print(f"\nYou : {text}")

    return text