import cv2
import numpy as np
from PyQt4 import QtGui

class playDemoVideo():
    def __init__(self,file):
        self.capture = cv2.VideoCapture(file)

    def captureRawFrame(self):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        #ret = self.capture.set(3, 640)
        #ret = self.capture.set(4, 480)
        ret, rawFrame = self.capture.read()
        if (ret == True):

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
            img = img.scaledToHeight(480)
            img = img.scaledToWidth(360)
            #self.previousFrame = self.currentFrame
            return img
        except:
            return None
