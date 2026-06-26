import os

from dotenv import load_dotenv

load_dotenv()


DEEPGRAM_API_KEY = os.getenv(
    "DEEPGRAM_API_KEY"
)


SAMPLE_RATE = 16000

CHANNELS = 1

CHUNK_SIZE = 1024

ENCODING = "linear16"

LANGUAGE = "en"