from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
import time

ROBOT_IP = "192.168.2.200"  # <- IP vom UR5
rtde_c = RTDEControlInterface(ROBOT_IP)
rtde_r = RTDEReceiveInterface(ROBOT_IP)

# Move to joint position
# joint_pos={

                                                            
#joint_q = [0, -1.57, 1.57, -1.57, -1.57, 1.57]
#joint_q = [0, -1.57, 1.57, -1.57, -1.57, 0.0]
joint_q = [-0.2713, -1.5946, 1.5636, -1.5399, -1.5708, 1.2995]
rtde_c.moveJ(joint_q)


# Hole aktuelle TCP-Position
tcp_pose = rtde_r.getActualTCPPose()
print("TCP Position:", tcp_pose)

# Stop
rtde_c.stopScript()