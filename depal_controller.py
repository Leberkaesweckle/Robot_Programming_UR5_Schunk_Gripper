import pygame
from depaletieren import Depaletieren

import time 
# Pygame initialisieren
pygame.init()
pygame.joystick.init()

# Prüfen, ob ein Joystick erkannt wurde
if pygame.joystick.get_count() == 0:
    print("Kein Controller erkannt.")
    exit()

# Den ersten erkannten Joystick verwenden
joystick = pygame.joystick.Joystick(0)
joystick.init()

Depal = Depaletieren()






print(f"Verbunden mit: {joystick.get_name()}")
print("Warte auf Eingaben... (Strg+C zum Beenden)")

# Button-Mapping (anpassbar je nach Controller)
button_map = {
    0: 'A',
    1: 'B',
    2: 'X',
    3: 'Y',
    4: 'L1',
    5: 'R1',
    6: 'Select',
    7: 'Start',
    8: 'L3',
    9: 'R3'
}

hat_map = {
    (0, 1): 'D-Pad Up',
    (0, -1): 'D-Pad Down',
    (-1, 0): 'D-Pad Left',
    (1, 0): 'D-Pad Right',
    (0, 0): 'D-Pad Neutral'
}

try:
    while True:
        for event in pygame.event.get():
            # Button gedrückt oder losgelassen
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button gedrückt: {button_map.get(event.button, f'Unbekannt ({event.button})')}")

                if event.button == 0:

                    Depal.simpletask()

                



            
                
                pygame.event.clear()

except KeyboardInterrupt:
    print("\nBeendet.")
finally:
    pygame.quit()
