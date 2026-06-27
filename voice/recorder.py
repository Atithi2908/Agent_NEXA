import tempfile
import time

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from voice.config import (
    SAMPLE_RATE,
    CHANNELS,
    CHUNK_SIZE,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
    MIN_RECORD_SECONDS,
    MAX_RECORD_SECONDS
)


class Recorder:

    def __init__(self):

        self.recording = False

        self.audio = []

    def record(self):

        input("\nPress ENTER to start recording...")

        print("\n🎤 Recording...")
        self.recording = True

        self.audio = []

        def callback(indata, frames, time_info, status):

            if status:
                print(status)

            if self.recording:
                self.audio.append(indata.copy())

        start_time = time.time()

        with sd.InputStream(

            samplerate=SAMPLE_RATE,

            channels=CHANNELS,

            dtype="int16",

            blocksize=CHUNK_SIZE,

            callback=callback

        ):

            # Compute how many chunks correspond to silence and minimum recording
            chunk_duration = CHUNK_SIZE / float(SAMPLE_RATE)
            silence_chunks_needed = max(1, int(SILENCE_DURATION / chunk_duration))
            min_chunks = max(1, int(MIN_RECORD_SECONDS / chunk_duration))

            while True:
                time.sleep(0.1)

                elapsed = time.time() - start_time
                if elapsed > MAX_RECORD_SECONDS:
                    print("\n⏱️ Max recording duration reached.")
                    break

                if len(self.audio) < silence_chunks_needed:
                    continue

                # Stack recent chunks and compute RMS
                recent = np.vstack(self.audio[-silence_chunks_needed:]).astype("float32")
                rms = np.sqrt(np.mean(recent ** 2))

                if rms < SILENCE_THRESHOLD and len(self.audio) >= min_chunks:
                    # Detected sustained silence
                    break

            self.recording = False

        if not self.audio:
            # No audio captured
            return ""

        audio = np.vstack(self.audio).astype("int16")

        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

        write(temp.name, SAMPLE_RATE, audio)

        print("\n✅ Recording Finished")

        return temp.name