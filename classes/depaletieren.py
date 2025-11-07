import ast
import numpy as np

from run_actions import UR5e_Gripper_Class



class Depaletieren:
    
    UR5e_Gripper = UR5e_Gripper_Class()  # Importiere die Gripper-Klasse

    def __init__(self):
        self.offset_grip_first_cup = np.array([0.0, 0.0, 0.0])
        self.offset_drop_first_cup = np.array([0.0, 0.0, 0.0])
        self.distance_between_cups_x = np.array([0.1138, 0.0, 0.0])
        self.distance_between_cups_y = np.array([0.0, 0.115, 0.0])

        self.file_path_grip = "grip_moves.txt"
        
        self.file_path_pos = "pos.txt"  # Optional, da aktuell ungenutzt

        self.file_path_move = "move.txt"
        self.file_path_drop = "drop.txt"

    def grip_cup(self, increment_x=1, increment_y=1):
        # Berechne absolute Position des Griffs
       
        result = []

        with open(self.file_path_pos, "r") as file:
            
                lines = file.readlines()
                for line in lines:
                    increment = ast.literal_eval(line.strip())

        increment_x = increment[0]
        increment_y = increment[1]


        pos_increment = (self.offset_grip_first_cup +
               self.distance_between_cups_x * increment_x +
               self.distance_between_cups_y * increment_y)
        
        try:
            with open(self.file_path_grip, "r") as file:
                
                for line in file:
                    try:
                        input = ast.literal_eval(line.strip())
                        pos = np.array(input[0:3]) + np.array(pos_increment)
                        pos_gripper = input[3]  # Addiere die berechnete Position
                        adjusted_pos = pos
                        adjusten_entry = adjusted_pos.tolist() + [pos_gripper]  # Füge den Gripper-Status hinzu
                                               
                        self.UR5e_Gripper.action_move(adjusten_entry)


                    except Exception as e:
                        print(f"Error parsing line: {line.strip()} -> {e}")
        except FileNotFoundError:
            print(f"File not found: {self.file_path_grip}")

        

        # Optional: Ausgabe zur Kontrolle
        for idx, item in enumerate(result):
            print(f"Position {idx + 1}: {item}")       

        self.update_increment(increment_x, increment_y)


        

        return result
    
    def update_increment(self, increment_x, increment_y):
        """Aktualisiert die Inkremente für die nächste Griffposition."""
        if increment_x == 4:
            increment_x  = 0
            

            if increment_y == 2:
                increment_y = 0

            else:
                increment_y += 1

        else:
            increment_x +=1




        
           

        ## Save in file
        with open(self.file_path_pos, "w") as file:
            file.write(f"[{increment_x}, {increment_y}]\n")
        
    

    def drop_cup(self):

        with open(self.file_path_drop, "r") as file:
            for line in file:
                input = ast.literal_eval(line.strip())
                self.UR5e_Gripper.action_move(input)

        
        pass

    def move_cup(self):

        with open(self.file_path_move, "r") as file:                
                for line in file:
                    input = ast.literal_eval(line.strip())
                    self.UR5e_Gripper.action_move(input)


    def simpletask(self):
        self.grip_cup()
        self.move_cup()
        self.drop_cup()  # Uncomment if drop_cup is implemented



    
        

if __name__ == "__main__":
    depal = Depaletieren()
    depal.grip_cup()
    depal.move_cup()
    depal.drop_cup()  # Uncomment if drop_cup is implemented


