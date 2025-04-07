import os.path


from bkstools.bks_lib.bks_base import BKSBase, keep_communication_alive_input, keep_communication_alive_sleep
from pyschunk.generated.generated_enums import eCmdCode
import time
from bkstools.scripts.bks_grip import WaitGrippedOrError

host = "192.168.2.105"
bksb = BKSBase(host)

def my_input( prompt ):
        '''alias
        '''
        return keep_communication_alive_input( bksb, prompt )

def my_sleep( t ):
        '''alias
        '''
        return keep_communication_alive_sleep( bksb, t )




for x in range(1):

    bksb.command_code = eCmdCode.CMD_ACK
    time.sleep(0.1)
    print("Bewegung")
    print(x)
    print
    #--- Open gripper by moving to an absolute postion:
    bksb.set_force = 100 # target position at 30 mm (distance between fingers)
    bksb.set_vel =  0.0 # target velocity limited to 50 mm/s  
    bksb.grp_dir = False
    bksb.command_code = eCmdCode.MOVE_FORCE 
    
    my_sleep(2)




   
   
    my_sleep(2)
