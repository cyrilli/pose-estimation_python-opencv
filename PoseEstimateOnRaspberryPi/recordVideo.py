# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 17:06:07 2016

@author: li_ch
"""

from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from PyQt4 import QtGui

class recordVideo():
    def __init__(self):
        # initialize the video stream and allow the camera
        # sensor to warmup
        self.vs = VideoStream(usePiCamera=1 > 0).start()
        time.sleep(2.0)
        self.currentFrame = np.array([])
        self.raw_img = np.array([])
        
        self.writer = None
        (h, w) = (None, None)
        
    def captureRawFrame(self):
        """
        capture frame and reverse RBG BGR and return opencv image, and also record the video
        """
        rawFrame = self.vs.read()
        rawFrame = imutils.resize(rawFrame, width=640)
        self.raw_img = rawFrame
        #return rawFrame

    def initRecord(self):
        if self.writer == None:
            # store the image dimensions, initialzie the video writer,
            # and construct the zeros array
            #(h, w) = self.raw_img.shape[:2]
            self.writer = cv2.VideoWriter('./demoVideo/'+str(int(time.time()))+'.avi', cv2.cv.FOURCC(*"XVID"), 15,
			(640 , 480 ), True)
    def record(self):
        # write the output frame to file
        self.writer.write(self.raw_img)

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
