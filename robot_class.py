from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
import torch



class Robot_Class:
    def __init__(self, ROBOT_IP = "192.168.2.200" ):
        self.ROBOT_IP = ROBOT_IP
        self.rtde_c = RTDEControlInterface(ROBOT_IP)
        self.rtde_r = RTDEReceiveInterface(ROBOT_IP)


    def set_pos_xyz(self, pos):
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = pos[0]
        soll_tcp_pose[1] = pos[1]
        soll_tcp_pose[2] = pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3]
        soll_tcp_pose[4] = ist_tcp_pose[4]
        soll_tcp_pose[5] = ist_tcp_pose[5]

        self.rtde_c.moveL(soll_tcp_pose,0.05,0.05)
        pass

    def append_pos_xyz(self, pos):        
        ist_tcp_pose = self.rtde_r.getActualTCPPose()
        soll_tcp_pose = [0,0,0,0,0,0]
        soll_tcp_pose[0] = ist_tcp_pose[0] + pos[0]  
        soll_tcp_pose[1] = ist_tcp_pose[1] + pos[1]
        soll_tcp_pose[2] = ist_tcp_pose[2] + pos[2]
        soll_tcp_pose[3] = ist_tcp_pose[3] 
        soll_tcp_pose[4] = ist_tcp_pose[4]
        soll_tcp_pose[5] = ist_tcp_pose[5] 

        self.rtde_c.moveL(soll_tcp_pose, 0.1, 0.1)
        pass


    def get_pos_xyz(self):
        return torch.tensor(self.rtde_r.getActualTCPPose(), device = "cpu")
    

    def set_home_pos(self):
        self.rtde_c.moveJ([-0.2713, -1.5946, 1.5636, -1.5399, -1.5708, 1.2995])
        pass



if __name__ == "__main__":
    robot = Robot_Class()
    
    pos = [-0.1,0,0]
    robot.append_pos_xyz(pos)

    