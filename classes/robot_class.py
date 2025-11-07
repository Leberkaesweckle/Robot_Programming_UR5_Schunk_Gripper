from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
import torch



class Robot_Class:
    def __init__(self, ROBOT_IP = "192.168.2.200", only_jog = False):
        """Initialisiert die Robot_Class mit der angegebenen ROBOT_IP und stellt eine Verbindung zum Roboter her."""
        self.ROBOT_IP = ROBOT_IP
        self.connect()

        self.only_jog = only_jog
        self.move_factor = 0.4 
        self.acc = 0.2
        self.x_max = 0.85
        self.x_min = -0.85
        self.y_max = 0.85
        self.y_min = -0.85
        self.z_max = 0.85
        self.z_min = 0.0029
        self.sphere_radius = 0.9

        self.inner_x_max = 0.20
        self.inner_x_min = -0.20
        self.inner_y_min = 0.20
        self.inner_y_max = -0.20

        self.last_move_jog = None   
        
        self.force_max_x = 20
        self.force_max_y = 20
        self.force_max_z = 30
        self.force_max_reset_x = 25
        self.force_max_reset_y = 25
        self.force_max_reset_z = 35
        self.reset_jog_value = 0.00
        self.max_reset_jog_value = 0.35
        self.torque_max = 5.0


    def connect(self):
        """Stellt eine Verbindung zum Roboter her, falls noch keine besteht."""
        if hasattr(self, 'rtde_c'):
            if self.rtde_c.isConnected() and self.rtde_r.isConnected():
                return       

        self.rtde_c = RTDEControlInterface(self.ROBOT_IP)
        self.rtde_r = RTDEReceiveInterface(self.ROBOT_IP)


    def set_pos_xyz(self, pos):
        """Setzt die Position des Roboters auf die angegebenen Koordinaten."""        
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = pos[0]
        soll_tcp_pose[1] = pos[1]
        soll_tcp_pose[2] = pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3]
        soll_tcp_pose[4] = ist_tcp_pose[4]
        soll_tcp_pose[5] = ist_tcp_pose[5]

        self.moveL_xyz(soll_tcp_pose, 0.1,0.1, True)
        pass

    def append_pos_xyz(self, pos):
        """Fügt die angegebenen Koordinaten zur aktuellen Position des Roboters hinzu."""        
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = ist_tcp_pose[0] + pos[0]  
        soll_tcp_pose[1] = ist_tcp_pose[1] + pos[1]
        soll_tcp_pose[2] = ist_tcp_pose[2] + pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3] + pos[3]
        soll_tcp_pose[4] = ist_tcp_pose[4] + pos[4]
        soll_tcp_pose[5] = ist_tcp_pose[5] + pos[5]

        self.moveL_xyz(soll_tcp_pose, 0.1,0.1)
        pass

    def append_pos_xyz_async(self, pos):
        """Fügt die angegebenen Koordinaten asynchron zur aktuellen Position des Roboters hinzu."""
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = ist_tcp_pose[0] + pos[0]  
        soll_tcp_pose[1] = ist_tcp_pose[1] + pos[1]
        soll_tcp_pose[2] = ist_tcp_pose[2] + pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3] + pos[3]
        soll_tcp_pose[4] = ist_tcp_pose[4] + pos[4]
        soll_tcp_pose[5] = ist_tcp_pose[5] + pos[5]

        self.moveL_xyz(soll_tcp_pose, 0.1,0.1, True)
        pass

    def set_pos_xyz_async(self, pos):
        """Setzt die Position des Roboters asynchron auf die angegebenen Koordinaten."""
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = pos[0]
        soll_tcp_pose[1] = pos[1]
        soll_tcp_pose[2] = pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3]
        soll_tcp_pose[4] = ist_tcp_pose[4]
        soll_tcp_pose[5] = ist_tcp_pose[5]

        self.moveL_xyz(soll_tcp_pose, 0.1,0.1, True)
        pass

    def set_jogStart(self, move):
        """Startet die Jog-Bewegung des Roboters mit den angegebenen Bewegungswerten."""       
        
        soll_move = [0,0,0,0,0,0]
        soll_move[0] = move[0] * self.move_factor
        soll_move[1] = move[1] * self.move_factor
        soll_move[2] = move[2] * self.move_factor
        soll_move[3] = move[3] * self.move_factor
        soll_move[4] = move[4] * self.move_factor
        soll_move[5] = move[5] * self.move_factor

        move = self.apply_save_range(soll_move[0],soll_move[1],soll_move[2], soll_move[3], soll_move[4], soll_move[5])
        self.last_move_jog = move
        self.rtde_c.jogStart(speeds = move, acc = self.acc)
        pass

    def set_acc_higer(self):
        self.acc = self.acc + 0.01
        if self.acc > 0.2:
            self.acc = 0.2
        print(f"Acceleration set to {self.acc}"
              )
        self.move_factor = self.move_factor +0.1
        if self.move_factor > 1:
            self.move_factor = 1
        print(f"Move factor set to {self.move_factor}"
              )
        
    def set_acc_lower(self):
        self.acc = self.acc - 0.01
        if self.acc < 0.05:
            self.acc = 0.05
        print(f"Acceleration set to {self.acc}"
              )
        
        self.move_factor = self.move_factor -0.1
        if self.move_factor < 0.1:
            self.move_factor = 0.1
        print(f"Move factor set to {self.move_factor}")


    def moveL_xyz(self, pos, vel = 0.1, acc = 0.1, asyncmode = False):

        if self.only_jog:
            print("Only jog mode active, moveL_xyz skipped")
            return
        
        """Bewegt den Roboter linear zu den angegebenen Koordinaten mit der angegebenen Geschwindigkeit und Beschleunigung."""
        
        try: 
            self.rtde_c.jogStop()
            move = self.apply_save_range(pos[0], pos[1], pos[2],0,0,0)
            done = self.rtde_c.moveL(pos,vel,acc, asyncmode)
        except Exception as e:
            print(f"Error in moveL_xyz: {e}")
            self.connect()
        pass
        if done == False:
            print("MoveL not done")
            ##self.connect()

    def get_last_action(self):
        """Gibt die letzte Jog-Bewegung des Roboters zurück."""
        return self.last_move_jog

    def get_pos_xyz(self):
        """Gibt die aktuelle Position des Roboters zurück."""
        return torch.tensor(self.rtde_r.getActualTCPPose(), device = "cpu")
    
    def set_home_pos(self):
        """Setzt den Roboter in die Home-Position zurück. Reset Jog wird aufgerufen."""
        self.rtde_c.jogStop()
        self.rtde_c.moveJ([-0.2713, -1.5946, 1.5636, -1.5399, -1.5708, 1.2995],acceleration = 0.1)
        pass


   
    

    ##Function that sets values that are lower than a threshold to zero
    def apply_deadzone(self,value, threshold=0.01):
        """Wendet eine Totzone auf den angegebenen Wert an. Werte unterhalb des Schwellenwerts werden auf Null gesetzt."""
        if abs(value) < threshold:
            return 0.0
        return value
    
    

    def apply_save_range(self,x,y,z,u,v,w):

        """Wendet Sicherheitsprüfungen auf die angegebenen Bewegungswerte an und gibt die angepassten Werte zurück."""

        pos = self.get_pos_xyz()

      

        ###Force check

        
        forces = self.get_force()

        x_force = forces[0]
        y_force = forces[1]
        z_force = forces[2]
        u_force = forces[3]
        v_force = forces[4]
        w_force = forces[5]

        ### Force limits 
        if x_force > self.force_max_x:
            if x < 0:
                x = self.reset_jog_value

        if x_force < -self.force_max_x:
            if x > 0:
                x = -self.reset_jog_value

        if y_force > self.force_max_y:
            if y < 0:
                y = self.reset_jog_value

        if y_force < -self.force_max_y:
            if y > 0:
                y = -self.reset_jog_value

        if z_force > self.force_max_z:
            if z < 0:
                z = self.reset_jog_value

        if z_force < -self.force_max_z:
            if z > 0:
                z = -self.reset_jog_value

        ### Max force limits for reset, moves away from obstacle if limit exceeded
        if x_force > self.force_max_reset_x:            
            x = self.max_reset_jog_value

        if x_force < -self.force_max_reset_x:
            x = -self.max_reset_jog_value
        
        if y_force > self.force_max_reset_y:
            y = self.max_reset_jog_value
        
        if y_force < -self.force_max_reset_y:
            y = -self.max_reset_jog_value
        
        if z_force > self.force_max_reset_z:
            z = self.max_reset_jog_value
        
        if z_force < -self.force_max_reset_z:
            z = -self.max_reset_jog_value


         ###Cube check

        if (pos[0] + x) > self.x_max or (pos[0] + x) < self.x_min:
            x = 0
        if (pos[1] + y) > self.y_max or (pos[1] + y) < self.y_min:
            y = 0
        if (pos[2] + z) > self.z_max or (pos[2] + z) < self.z_min:
            z = 0

        ###Sphere check
        if torch.sqrt((pos[0] + x)**2 + (pos[1] + y)**2 + (pos[2] + z)**2) > self.sphere_radius:
            x = 0
            y = 0
            z = 0
        

        ###Inner square check robot should not enter
        if (pos[0] + x) < self.inner_x_max and (pos[0] + x) > self.inner_x_min:
            if (pos[1] + y) < self.inner_y_min and (pos[1] + y) > self.inner_y_max:
                x = 0
                y = 0


        

        move = [x,y,z,u,v,w]
        return move
    
    def set_jogStop(self):
        """Stoppt die Jog-Bewegung des Roboters."""
        self.rtde_c.jogStop()
        pass

    def get_force(self):
        """Gibt die aktuelle TCP-Kraft des Roboters zurück."""
        return self.rtde_r.getActualTCPForce()
    
    def disconnect(self):
        """Trennt die Verbindung zum Roboter."""
        if hasattr(self, 'rtde_c'):
            self.rtde_c.disconnect()
        if hasattr(self, 'rtde_r'):
            self.rtde_r.disconnect()


        pass
            


        



if __name__ == "__main__":
    robot = Robot_Class()
    print("Roboer Class created")
    print("Current Position of Robot:")
    print(robot.get_pos_xyz())
    
    #pos = [-0.1,0,0]
    #robot.append_pos_xyz(pos)

    