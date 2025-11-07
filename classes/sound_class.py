import pygame
from pathlib import Path
pygame.init()
pygame.mixer.init()


class sounds():
    def __init__(self):
        start_sound_file = Path("classes") / "Assets" / "game-start-317318.mp3"
        self.sound_start = pygame.mixer.Sound(str(start_sound_file))
        #classes\Assets\game-start-317318.mp3
        self.sound_start.set_volume(1)



    def play_sound_start(self):
        self.sound_start.play()

    def play_horn(self):
        horn_file = Path("classes")/ "Assets" / "Horn.wav"
        self.sound_horn = pygame.mixer.Sound(str("classes/assets/Horn.wav"))
        self.sound_horn.set_volume(1)
        self.sound_horn.play()   


#sound = sounds()
#sound.play_sound_start()
#sound.play_horn()