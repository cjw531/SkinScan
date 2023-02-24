from abc import ABC
# import tkinter
from PIL import Image, ImageTk
import numpy as np
import cv2
import time
# if using an environment different to PyCharm
# import sys
# sys.path.insert(0,'..')
import warnings
warnings.filterwarnings("ignore", message="module not found")
from Projection import Projection

class Screen(Projection, ABC):
    def __init__(self, frequency=0, monitor_list=None, monitor_index=0):
        self.projection_monitor = monitor_list[monitor_index] # connected monitors

        print("Screen resolution: ", (self.projection_monitor.width, self.projection_monitor.height))
        resolution = (self.projection_monitor.width, self.projection_monitor.height)

        # Init base class
        super().__init__(resolution, frequency)
        self.count = 0
        # Create empty pattern and camera
        self.pattern = None
        self.camera = None

    def displayCalibrationPattern(self, camera, path_calib='CalibrationImages/8_24_checker.png',
                                  save_img='Geometric/geo'):
        self.camera = camera
        img = cv2.imread(path_calib)
        cv2.namedWindow('Checkerboard', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Checkerboard', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Checkerboard', img)
        time.sleep(2)
        self.camera.getImage(name=save_img, calibration=True)
        cv2.waitKey(0)  # any key
        cv2.destroyWindow('Checkerboard')

    def displayPatterns(self, camera):
        # Displays a series of pattern, which is updated in updateCanvas
        # If you only desire to view the projection, pass on None for the input camera
        self.camera = camera
        cv2.waitKey(100)
        self.update_opencv_window()

    def setPattern(self, pattern):
        # Sets pattern to project
        self.pattern = pattern

    # TODO: Deprecated, original pattern projection code with tkinter
    '''
    def updateCanvas(self):
        # Updates the pattern to project
        if self.count >= self.pattern.patterns.shape[-1]:
            # If done, quit projection
            self.root.destroy()
            return
        # Create Pil image from Np array
        modulation = self.pattern.patterns[..., self.count]*255
        pilImage = Image.fromarray(modulation.astype(np.uint8))
        image = ImageTk.PhotoImage(pilImage)
        # Set image
        self.canvas.create_image(0, 0, anchor='nw', image=image)
        self.root.update()
        time.sleep(2)
        if self.camera is None:
            print("No camera initialized.")
        else:
            # Take snapshot
            if self.camera.hdr_exposures is None:
                self.camera.getImage(name='capture_'+str(self.count))
            else:
                self.camera.getHDRImage(name='capture_'+str(self.count))
        self.count += 1
        self.root.after(100, self.updateCanvas())
    '''

    def update_opencv_window(self):
        # Updates the pattern to project
        if self.count >= self.pattern.patterns.shape[-1]:
            # If done, quit projection
            cv2.destroyAllWindows()
            return
        
        modulation = (self.pattern.patterns[..., self.count] * 255).astype(np.uint8)
        window_name = 'Pattern'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.imshow(window_name, modulation)
        cv2.moveWindow(window_name, self.projection_monitor.x, self.projection_monitor.y)
        cv2.resizeWindow(window_name, self.projection_monitor.width, self.projection_monitor.height)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        time.sleep(2)
        if self.camera is None:
            print("No camera initialized.")
        else:
            # Take snapshot
            if self.camera.hdr_exposures is None:
                self.camera.getImage(name='capture_'+str(self.count))
            else:
                self.camera.getHDRImage(name='capture_'+str(self.count))
        self.count += 1
        cv2.waitKey(100)
        self.update_opencv_window()

    def getResolution(self):
        # Returns tuple of resolution (width x height)
        return self.resolution

    def setResolution(self, resolution):
        # Sets tuple of resolution (width x height)
        self.resolution = resolution

    def quit_and_close(self):
        # Close the projection
        cv2.destroyAllWindows()
