import pygame
from classes.gripper_class import Schunk_Gripper
from classes.robot_class import Robot_Class
from classes.txt_io_class import TxtIOClass
from classes.camera_class import camera_class

import time
import threading

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

# Shared state (einfacher Dict)
latest_state = {
    "pos": Robot.get_pos_xyz()[0:3],
    "jog": Robot.get_last_action(),
    "go": False,
    "gc": False,
    "frame": 0
}

### Kamera Logging aktivieren/deaktivieren
log_camera = False

### Kamera Konfiguration
serial_robot = "825312071832"
serial_context = "825312071649"

### Pfad zum Speichern der Bilder
log_path = r"V:\Inst_NCT\AUT\99_Transfer\VLAM_Data_Generation_LNDW"

# Kamera-Objekte (werden initialisiert falls log_camera True)
camera_robot = None
camera_context = None

if log_camera:
    print("Starte Kameras...")
    camera_robot = camera_class(
        serial_camera=serial_robot,
        camera_name="robot",
        save_path=log_path,
        number_of_frame=0,
        depth_active=False
    )
    camera_context = camera_class(
        serial_camera=serial_context,
        camera_name="context",
        save_path=log_path,
        number_of_frame=0,
        depth_active=False,
        folder_path=camera_robot.get_folder_path()
    )
    print("Kameras gestartet.")

print(f"Verbunden mit: {joystick.get_name()}")

print("Warte auf Eingaben... (Strg+C zum Beenden)")

# Kleine helper-Funktion: starte einen kurzen Daemon-Thread, der einmal capture_frame aufruft
def async_capture_once(camera_obj, state_copy, thread_name=None):
    def _worker():
        try:
            camera_obj.capture_frame(
                pos=state_copy["pos"],
                jog=state_copy["jog"],
                go=state_copy["go"],
                gc=state_copy["gc"],
                number_of_frame=state_copy["frame"]
            )
        except Exception as e:
            name = thread_name or "camera_worker"
            print(f"[{name}] Fehler beim capture_frame: {e}")
    t = threading.Thread(target=_worker, daemon=True)
    t.start()

# Button- / Hat- Maps
button_map = {
    0: 'A',
    1: 'B',
    2: 'X',
    3: 'Y',
    10: 'Minus',
    11: 'Select',  # deine Taste 11
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

scale = 0.1

try:
    while True:
        # Joystick-Achsen
        x = joystick.get_axis(4)  # X-Achse
        y = joystick.get_axis(3)  # Y-Achse
        z = joystick.get_axis(1)  # Z-Achse

        x = Robot.apply_deadzone(x)
        y = Robot.apply_deadzone(y)
        z = Robot.apply_deadzone(z)

        open_gripper = False
        close_gripper = False

        Robot.set_jogStart([x * scale * -1, y * scale * -1, z * scale * -1, 0, 0, 0])

        for event in pygame.event.get():
            # Button gedrückt oder losgelassen
            if event.type == pygame.JOYBUTTONDOWN:
                btn_name = button_map.get(event.button, f'Unbekannt ({event.button})')
                print(f"Button gedrückt: {btn_name}")

                if event.button == 1:
                    Gripper.close_gripper()
                    close_gripper = True

                elif event.button == 0:
                    Gripper.open_gripper()
                    open_gripper = True

                elif event.button == 11:
                    # Taste 11: Kameras neu initialisieren (neue Instances)
                    Robot.set_home_pos()
                    Gripper.open_gripper_wait()
                    latest_state["frame"] = 0
                    print("Taste 11 gedrückt: Kameras werden neu gestartet...")
                    if log_camera:
                        try:
                            camera_robot = camera_class(
                                serial_camera=serial_robot,
                                camera_name="robot",
                                save_path=log_path,
                                number_of_frame=0,
                                depth_active=False
                            )
                            camera_context = camera_class(
                                serial_camera=serial_context,
                                camera_name="context",
                                save_path=log_path,
                                number_of_frame=0,
                                depth_active=False,
                                folder_path=camera_robot.get_folder_path()
                            )
                            print("Kameras neu initialisiert.")
                        except Exception as e:
                            print(f"Fehler beim Neustart der Kameras: {e}")

                elif event.button == 10:
                    Robot.connect()

                elif event.button == 6:
                    print(Robot.get_pos_xyz()[0:3])
                    print(Gripper.get_gripper_pos_binary())
                    TXT_Ouput.append_tasks([Robot.get_pos_xyz()[0:3].tolist() + [Gripper.get_gripper_pos_binary()]])

                elif event.button == 8:
                    Robot.append_pos_xyz([0, 0, 0.005])
                elif event.button == 9:
                    Robot.append_pos_xyz([0, 0, -0.005])

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button losgelassen: {button_map.get(event.button, f'Unbekannt ({event.button})')}")

            elif event.type == pygame.JOYHATMOTION:
                print(f"D-Pad: {hat_map.get(event.value, f'Unbekannt {event.value}')}")
                if event.value == (0, 1):
                    Robot.append_pos_xyz([0.005, 0, 0])
                elif event.value == (0, -1):
                    Robot.append_pos_xyz([-0.005, 0, 0])
                elif event.value == (-1, 0):
                    Robot.append_pos_xyz([0, 0.005, 0])
                elif event.value == (1, 0):
                    Robot.append_pos_xyz([0, -0.005, 0])

            # clear events falls nötig
            # pygame.event.clear()  # optional hier deaktiviert, weil wir bereits events iterieren

        # Kamera-Logik: Zustand updaten und pro Kamera einen kurzen Thread starten
        if log_camera and camera_robot is not None and camera_context is not None:
            latest_state["pos"] = Robot.get_pos_xyz()[0:3]
            latest_state["jog"] = Robot.get_last_action()
            latest_state["go"] = open_gripper
            latest_state["gc"] = close_gripper
            latest_state["frame"] += 1

            state_copy = latest_state.copy()
            # zwei kurze Daemon-Threads; sie beenden sich nach dem capture automatisch
            async_capture_once(camera_robot, state_copy, thread_name="robot_cam_once")
            async_capture_once(camera_context, state_copy, thread_name="context_cam_once")
            time.sleep(0.05)
                    

except KeyboardInterrupt:
    print("\nBeendet.")
    Robot.set_jogStop()
    Robot.disconnect()
    
finally:
    Robot.set_jogStop()
    Robot.disconnect()
    pygame.quit()
