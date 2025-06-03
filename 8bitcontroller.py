import pygame
from gripper_class import Schunk_Gripper
from robot_class import Robot_Class
from txt_io_class import TxtIOClass

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
TXT_Ouput = TxtIOClass(file_path="output.txt")





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

                if event.button == 7:
                    Robot.set_home_pos()

                if event.button == 6:
                    
                    print(Robot.get_pos_xyz()[0:3])
                    print(Gripper.get_gripper_pos_binary())
                    TXT_Ouput.append_tasks([Robot.get_pos_xyz()[0:3].tolist() + [Gripper.get_gripper_pos_binary()]])


                





                    
                    

                if event.button == 4:
                    Robot.append_pos_xyz([0,0,0.005])
                if event.button == 5:
                    Robot.append_pos_xyz([0,0,-0.005])

                

                

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button losgelassen: {button_map.get(event.button, f'Unbekannt ({event.button})')}")

                ##Achse 0 = Z Achse
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
                Robot.append_pos_xyz([x*scale*-1, y*scale*-1, z*scale*-1])
                pygame.event.clear()


            

            # D-Pad (HAT) Eingaben
            elif event.type == pygame.JOYHATMOTION:
                print(f"D-Pad: {hat_map.get(event.value, f'Unbekannt {event.value}')}")
                if event.value == (0, 1):
                    print("D-Pad Up")
                    Robot.append_pos_xyz([0.005,0,0])
                elif event.value == (0, -1):
                    print("D-Pad Down")
                    Robot.append_pos_xyz([-0.005,0,0])
                elif event.value == (-1, 0):
                    print("D-Pad Left")
                    Robot.append_pos_xyz([0,0.005,0])
                elif event.value == (1, 0):
                    print("D-Pad Right")
                    Robot.append_pos_xyz([0,-0.005,0])



            
                
            pygame.event.clear()

except KeyboardInterrupt:
    print("\nBeendet.")
finally:
    pygame.quit()
