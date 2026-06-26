import tempfile

import sounddevice as sd
from scipy.io.wavfile import write

from voice.config import (
    SAMPLE_RATE,
    CHANNELS
)


class Recorder:

    def __init__(self):

        self.recording = False

        self.audio = []

    def record(self):

        input(
            "\nPress ENTER to start recording..."
        )

        print("\n🎤 Recording...")
        print("Press ENTER again to stop.")

        self.recording = True

        self.audio = []

        def callback(
            indata,
            frames,
            time,
            status
        ):

            if status:
                print(status)

            if self.recording:
                self.audio.append(
                    indata.copy()
                )

        with sd.InputStream(

            samplerate=SAMPLE_RATE,

            channels=CHANNELS,

            dtype="int16",

            callback=callback

        ):

            input()

            self.recording = False

        audio = self.audio[0]

        for chunk in self.audio[1:]:

            audio = __import__("numpy").vstack(
                (
                    audio,
                    chunk
                )
            )

        temp = tempfile.NamedTemporaryFile(

            suffix=".wav",

            delete=False

        )

        write(

            temp.name,

            SAMPLE_RATE,

            audio

        )

        print("\n✅ Recording Finished")

        return temp.name