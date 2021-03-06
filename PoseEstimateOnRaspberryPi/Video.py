import cv2
import numpy as np
from PyQt4 import QtGui
from imutils.video import VideoStream
import imutils
import time
class Video():
    def __init__(self):
        self.vs = VideoStream(usePiCamera=1 > 0).start()
        time.sleep(2.0)
        self.currentFrame = np.array([])
        self.raw_img = np.array([])


    def captureRawFrame(self):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        rawFrame = self.vs.read()
        rawFrame = imutils.resize(rawFrame, width=640)
        self.raw_img = rawFrame
        #return rawFrame

    def convertFrame(self):
        """
        converts frame to format suitable for QtGui
        """
        try:
            self.currentFrame = cv2.cvtColor(self.raw_img, cv2.COLOR_BGR2RGB)
            height, width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                               width,
                               height,
                               QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            #self.previousFrame = self.currentFrame
            img = img.scaledToHeight(480)
            img = img.scaledToWidth(360)
            return img
        except:
            return None
