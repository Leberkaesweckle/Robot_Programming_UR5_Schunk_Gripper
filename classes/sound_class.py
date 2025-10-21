import pygame
pygame.init()
pygame.mixer.init()

# Sound laden und abspielen
sound = pygame.mixer.Sound("beep.wav")
sound.play()

# Lautstärke ändern (0.0 bis 1.0)
sound.set_volume(0.5)