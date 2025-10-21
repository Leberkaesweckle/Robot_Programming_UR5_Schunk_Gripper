import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os
import time

class camera_class:

    
    def __init__(self,
                 serial_camera="825312071832", 
                 camera_name = "undefinde",    # hier deine echte SN eintragen                                
                 save_path=r"V:\Inst_NCT\AUT\99_Transfer\VLAM_Data_Generation_LNDW",
                 number_of_frame = 0,
                 depth_active = False,
                 folder_path = None
                 ):
        self.save_path = save_path
        self.number_of_frame = number_of_frame 
        self.depth_active = depth_active
        self.camera_name = camera_name

        if folder_path is None:
            self.make_new_folder(save_path=self.save_path)
        else:
            self.folder_path = folder_path

        # --- RealSense Kamera  ---
        self.pipeline_camera = rs.pipeline()
        self.config_camera = rs.config()
        self.config_camera.enable_device(serial_camera)
        self.config_camera.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        if self.depth_active:
            self.config_camera.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline_camera.start(self.config_camera)

        print("✅ RealSense-Kamera initialisiert.")


    def get_folder_path(self):
        return self.folder_path

    def make_new_folder(self, save_path=r"V:\Inst_NCT\AUT\99_Transfer\VLAM_Data_Generation_LNDW"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_path = os.path.join(save_path, f"capture_{timestamp}")
        os.makedirs(folder_path, exist_ok=True)
        folder_path = folder_path
        self.folder_path = folder_path
        print(f"📁 Neuer Ordner erstellt: {folder_path}")

        return folder_path

    def capture_frame(self, pos=None, jog=None, go=None, gc=None, number_of_frame=None):
        

        # --- Kamera  ---
        frames_camera = self.pipeline_camera.wait_for_frames()
        color_camera = np.asanyarray(frames_camera.get_color_frame().get_data())
        if self.depth_active:
            depth_camera = np.asanyarray(frames_camera.get_depth_frame().get_data())
       
        

        # --- Dateien speichern ---
        color_file_camera = os.path.join(
            self.folder_path,
            f"{self.camera_name}_color_{number_of_frame}_pos_{pos}_jog_{jog}_go{go}_gc{gc}.jpg")
        if self.depth_active:
            depth_file_camera = os.path.join(
                self.folder_path,
                f"{self.camera_name}_depth_{number_of_frame}.png")

        cv2.imwrite(color_file_camera, color_camera)
        if self.depth_active:
            cv2.imwrite(depth_file_camera, depth_camera)

        print(f"✅ Frame {self.camera_name}_{self.number_of_frame} gespeichert.")
        

    def stop(self):
        self.pipeline_camera.stop()
        print("🛑 Kamera gestoppt.")

if __name__ == "__main__":
    cams = camera_class(
        serial_camera="825312071832",     # hier deine echte SN eintragen
    )
    cams.make_new_folder()
    for i in range(3):
        start = time.time()
        cams.capture_frame()
        print(f"⏱️ Dauer: {time.time() - start:.2f}s")
    cams.stop()