from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface
import time

ROBOT_IP = "192.168.2.200"  # <- IP vom UR5
rtde_c = RTDEControlInterface(ROBOT_IP)
rtde_r = RTDEReceiveInterface(ROBOT_IP)

print("Connected to Robot")
tcp_pose = rtde_r.getActualTCPPose()
print("TCP Position:", tcp_pose)


