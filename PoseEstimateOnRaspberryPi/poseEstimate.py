# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

class poseEstimate():
    def __init__(self, frame, height, width, size, cmxDir):
        self.frame = frame
        self.rvec_str = ''
        self.tvec_str = ''
        self.height = height-1
        self.width = width-1
        self.size = size
        self.cmxDir = cmxDir
        self.err_str = ''
        
    def solvePnP(self):
        """
        已知相机标定参数，估计相机坐标系相对于棋盘格坐标系的旋转平移向量
        """
        frame = self.frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        objp = np.zeros((self.width * self.height, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.height, 0:self.width].T.reshape(-1, 2)
        objp = objp * self.size
        calib_data = np.load(self.cmxDir)
        cmx = calib_data['cmx']
        dist = calib_data['dist']
        #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        axis = self.size*np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.ret, corners = cv2.findChessboardCorners(grey, (self.height, self.width), None)
        if self.ret == 1:
            #corners2 = cv2.cornerSubPix(grey, corners, (11, 11), (-1, -1), criteria)
            ret, rvec, tvec = cv2.solvePnP(objp, corners, cmx, dist)
            imgpoints2, _ = cv2.projectPoints(objp, rvec, tvec, cmx, dist)
            error = cv2.norm(corners, imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            self.err_str = str(error)
            
            axis_img, _ = cv2.projectPoints(axis, rvec, tvec, cmx, dist)
            self.draw(frame, corners, axis_img)
            self.rvec_str = self.vec2str(rvec)
            self.tvec_str = self.vec2str(tvec)
            cv2.putText(frame, 'rvec:' + self.rvec_str, (20, 425), font, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, 'tvec:' + self.tvec_str, (20, 450), font, 0.8, (255, 255, 255), 2)
        else:
            cv2.putText(frame, 'No Chessboard Corners Detected!', (20, 425), font, 0.8, (255, 255, 255), 2)

        return frame


    def vec2str(self, vec):
        """
        用来把旋转平移向量转换为适合在屏幕上显示的字符串
        """
        result = ''
        for i in range(0, len(vec)):
            i_str = str(vec[i]).strip('[').strip(']')
            result = result + ' ' + i_str[:i_str.index('.')+5]
        return result

    def draw(self, img, corners, imgpts):
        """
        在图片上画出三根坐标轴
        """
        corner = tuple(corners[0].ravel())
        cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
        cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
        cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
        return img
