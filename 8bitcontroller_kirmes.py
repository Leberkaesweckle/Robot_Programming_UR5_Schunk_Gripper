import pygame
from gripper_class import Schunk_Gripper
from robot_class import Robot_Class
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

Gripper = Schunk_Gripper()
Robot = Robot_Class()


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
                    Gripper.close_gripper_wait()


                if event.button == 1: 
                    Gripper.open_gripper()

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button losgelassen: {button_map.get(event.button, f'Unbekannt ({event.button})')}")

                ##Achse 1 = Z Achse
                ##Achse 2 = X Achse
                ##Achse 3 = Y Achse

            

            # Achsenbewegung (Sticks, Trigger)
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Achse {event.axis} bewegt: {event.value:.2f}")
                scale = 0.1

                pygame.event.pump()
                time.sleep(0.01)
                

                # Joystick-Achsen live abfragen
                x = joystick.get_axis(2)  # X-Achse
                y = joystick.get_axis(3)  # Y-Achse
                z = joystick.get_axis(1)  # Z-Achse

                print(f"Joystick-Achsen: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
                Robot.append_pos_xyz([x*scale, y*scale, z*scale])
                pygame.event.clear()


            

            # D-Pad (HAT) Eingaben
            elif event.type == pygame.JOYHATMOTION:
                print(f"D-Pad: {hat_map.get(event.value, f'Unbekannt {event.value}')}")

except KeyboardInterrupt:
    print("\nBeendet.")
finally:
    pygame.quit()
