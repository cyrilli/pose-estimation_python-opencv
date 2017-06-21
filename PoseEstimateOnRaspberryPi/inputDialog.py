
# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import numpy as np
import cv2
import glob
import pdb

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class calibrateCamera():
    def __init__(self, img_list, height, width, cell_size):
        # Step 1: Data prep
        self.img_list = img_list
        # self.img_list = glob.glob('./chessboard/chessboard_gray*.jpg')
        self.img_list_detected = []
        self.cell_height = height-1
        self.cell_width = width-1
        self.cell_size = cell_size
        # set opts
        self.objp = np.zeros((self.cell_width*self.cell_height,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.cell_height,0:self.cell_width].T.reshape(-1,2)
        self.objp = self.objp * self.cell_size
        self.size = (self.cell_height, self.cell_width)

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.

    def calibration(self):

        for fname in self.img_list:
            img = cv2.imread(fname)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(grey, self.size, None)
            cv2.drawChessboardCorners(img, self.size, corners,ret)

            # if found, show imgs
            if ret:
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                cv2.cornerSubPix(grey,corners,(11,11),(-1,-1),criteria)
                self.imgpoints.append(corners)
                self.objpoints.append(self.objp)
                self.img_list_detected.append(fname)
                print fname

            cv2.imshow('img',img)
            cv2.waitKey(500)

        cv2.destroyAllWindows()


        # Step 2: Calibration
        # shape[::-1]: (480,640) => (640,480)
        ret, cmx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, grey.shape[::-1],None,None)
        print cmx
        print dist
        # save calibration result
        np.savez('./calibFile/calib.npz', cmx=cmx, dist=dist, rvecs=rvecs, tvecs=tvecs)

class InputDlg(QDialog):
    def __init__(self ,parent=None):
        super(InputDlg ,self).__init__(parent)
        self.setWindowIcon(QIcon('./icons/windowIcon.png'))
        self.height = 10
        self.width = 9
        self.size = 12
        label1=QLabel( self.tr("图片路径"))
        label2=QLabel( self.tr("棋盘格长（个）"))
        label3=QLabel( self.tr("棋盘格宽（个）"))
        label4=QLabel( self .tr("单格边长（毫米)"))

        self.heightLabel=QLabel("10")
        self.heightLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )
        self.widthLabel=QLabel("9")
        self.widthLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )
        self.sizeLabel=QLabel("12")
        self.sizeLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )

        picButton=QPushButton( u"选择图片文件")
        heightButton=QPushButton( u"修改")
        widthButton=QPushButton( u"修改")
        sizeButton=QPushButton( u"修改" )
        calibButton = QPushButton(u"开始标定")

        self.connect(picButton,SIGNAL( "clicked()"),self.slotPic)
        self.connect(heightButton,SIGNAL( "clicked()"),self.slotHeight)
        self.connect(widthButton,SIGNAL( "clicked()"),self.slotWidth)
        self.connect(sizeButton,SIGNAL( "clicked()"),self.slotSize)
        self.connect(calibButton, SIGNAL("clicked()"), self.calib)

        layout=QGridLayout()
        layout.addWidget(label1,0,0, 1,0)
        layout.addWidget(label2,2,0)
        layout.addWidget(label3,3,0)
        layout.addWidget(label4,4,0)
        layout.addWidget(self.heightLabel, 2, 1)
        layout.addWidget(self.widthLabel, 3, 1)
        layout.addWidget(self.sizeLabel, 4, 1)
        layout.addWidget (heightButton,2,2)
        layout.addWidget (widthButton,3,2)
        layout.addWidget (sizeButton,4,2)
        layout.addWidget(picButton, 0, 1, 1, 2)
        layout.addWidget(calibButton, 5,1, 5,2)

        self. setLayout( layout)

        self.setWindowTitle(self.tr("标定相机"))

    def slotPic(self):
        img_QStringList = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "All Files (*);;Text Files (*.jpg)")
        self.img_list = str(img_QStringList.join("<join>")).split("<join>")

    def slotHeight(self):
        h, ok = QInputDialog.getInteger(self, self.tr("棋盘格长"),
                                          self.tr("请输入棋盘格长（个）:"),
                                          int(self.heightLabel.text()), 0, 150)
        self.height = int(h)
        if ok:
            self.heightLabel.setText(str(h))

    def slotWidth(self):
        w,ok=QInputDialog. getInteger(self,self.tr("棋盘格宽"),
                                       self.tr("请输入棋盘格宽（个）:"),
                                       int(self. widthLabel. text()),0,150)

        self.width = int(w)
        if ok:
            self.widthLabel.setText(str(w))

    def slotSize(self):
        s,ok =QInputDialog.getDouble(self ,self.tr("棋盘格边长"),
                                          self.tr("请输入棋盘格边长（毫米）:"),
                                          float(self.sizeLabel.text()) ,0 ,150.00)
        self.size = float(s)
        if ok:
            self.sizeLabel.setText(str(s))

    def calib(self):
        calib = calibrateCamera(self.img_list, self.height, self.width, self.size)
        calib.calibration()
