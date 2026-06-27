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

# Silence detection / recording settings
SILENCE_THRESHOLD = 1000
# seconds of sustained silence required to stop recording
SILENCE_DURATION = 3

MIN_RECORD_SECONDS = 1.0
MAX_RECORD_SECONDS = 30