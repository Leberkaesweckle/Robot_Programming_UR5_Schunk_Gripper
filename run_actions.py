import ast  # für sicheres Parsen von Listen aus Strings
import time
from gripper_class import Schunk_Gripper
from robot_class import Robot_Class

# Pfad zur Datei (anpassen!)


class UR5e_Gripper_Class:

    def __init__(self):

        self.gripper = Schunk_Gripper()
        self.robot = Robot_Class()

    def read_tasks(self, dateipfad = "simple_task.txt"):
        

        daten = []

        with open(dateipfad, "r") as file:
            for zeile in file:
                try:
                    eintrag = ast.literal_eval(zeile.strip())  # wandelt Text in Liste um
                    daten.append(eintrag)
                except Exception as e:
                    print(f"Fehler beim Parsen: {zeile} -> {e}")

        # Ausgabe
        for eintrag in daten:
            print(eintrag)

        self.actions_list = daten

    def set_home_pos(self):
        self.robot.set_home_pos()
        time.sleep(1)


    def action(self):
        for x in self.actions_list:
            print("Bewegung")
            print(x)
            self.robot.set_pos_xyz(x[0:3])
            time.sleep(1)
            if x[3] == 0:
                self.gripper.open_gripper_wait()
                time.sleep(1)
            elif x[3] == 1:
                self.gripper.close_gripper_wait()
                time.sleep(1)


        

if __name__ == "__main__":
    ur5e_gripper = UR5e_Gripper_Class()
    ur5e_gripper.read_tasks()
    ur5e_gripper.set_home_pos()

    ur5e_gripper.action()
    


   