from rtde_io import RTDEIOInterface
from rtde_receive import RTDEReceiveInterface
from rtde_control import RTDEControlInterface
from rtde_control import RTDEControlInterface as RTDEControl
import time

UR_IP = "192.168.2.200"
io = RTDEIOInterface(UR_IP)

rcv = RTDEReceiveInterface(UR_IP)
#öffnen
io.setInputIntRegister(18, 1)
time.sleep(1)
#schließen
io.setInputIntRegister(18, 2)
time.sleep(1)
status_gripper = rcv.getOutputIntRegister(12)  # 1 = offen, 2 = zu etc.
#schließen
io.setInputIntRegister(18, 1)
time.sleep(1)
io.setInputIntRegister(20, 0)  # Geschwindigkeit
time.sleep(1)
io.setInputIntRegister(20, 1)  # Geschwindigkeit
time.sleep(1)
io.setInputIntRegister(20, 2)  # Geschwindigkeit
# status lesen (optional)
status_gripper = rcv.getOutputIntRegister(12)  # 1 = offen, 2 = zu etc.
status_vacuum = rcv.getOutputIntRegister(13)  # 1 = Vakuum an, 0 = Vakuum aus

print(f"Gripper status: {status_gripper}, Vakuum status: {status_vacuum}")