
from bkstools.bks_lib.bks_base import BKSBase, keep_communication_alive_input, keep_communication_alive_sleep
from pyschunk.generated.generated_enums import eCmdCode
import time
from bkstools.scripts.bks_grip import WaitGrippedOrError

class Schunk_Gripper():

    def __init__(self, host = "192.168.2.105"):

        self.bksb = BKSBase(host)
        
    def input(self,prompt ):
        '''alias
        '''
        return keep_communication_alive_input(self.bksb, prompt )
    
    def sleep(self,t):
        '''alias
        '''
        return keep_communication_alive_sleep(self.bksb,t)

    def close_gripper_wait(self):
        self.bksb.command_code = eCmdCode.CMD_ACK
        self.bksb.set_force = 100 
        self.bksb.set_vel =  0.0   
        self.bksb.grp_dir = False
        self.bksb.command_code = eCmdCode.MOVE_FORCE 
        WaitGrippedOrError( self.bksb )
        pass

    def open_gripper_wait(self):
        self.bksb.command_code = eCmdCode.CMD_ACK
        self.bksb.set_force = 100 
        self.bksb.set_vel =  0.0 
        self.bksb.grp_dir = True
        self.bksb.command_code = eCmdCode.MOVE_FORCE 
        WaitGrippedOrError( self.bksb )
        pass

    def open_gripper(self):
        self.bksb.command_code = eCmdCode.CMD_ACK
        self.bksb.set_force = 100 
        self.bksb.set_vel =  0.0 
        self.bksb.grp_dir = True
        self.bksb.command_code = eCmdCode.MOVE_FORCE 
        pass

    def close_gripper(self):
        self.bksb.command_code = eCmdCode.CMD_ACK
        self.bksb.set_force = 100 
        self.bksb.set_vel =  0.0   
        self.bksb.grp_dir = False
        self.bksb.command_code = eCmdCode.MOVE_FORCE 
        pass
    

    def set_position(self, position: float):
        self.bksb.set_pos = position
        self.bksb.set_vel =  50.0
        self.bksb.command_code = eCmdCode.MOVE_POS
        pass
    

    def action_gripper(self, action: bool):
        if action:
            self.open_gripper()
        else:
            self.close_gripper()
        pass

    def get_gripper_pos(self) -> float:
        return self.bksb.actual_pos





if __name__ == "__main__":
    gripper = Schunk_Gripper()
    for x in range(10):
        print("Bewegung")
        print(x)

        gripper.close_gripper_wait()
        
        gripper.open_gripper_wait()

    
    





    