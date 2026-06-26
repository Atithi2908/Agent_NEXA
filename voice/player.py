import pygame


class AudioPlayer:

    def __init__(self):

        pygame.mixer.init()

    def play(
        self,
        audio_file: str
    ):

        pygame.mixer.music.load(
            audio_file
        )

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            pygame.time.Clock().tick(
                10
            )