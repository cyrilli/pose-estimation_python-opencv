# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class settingDlg(QDialog):
    def __init__(self ,parent=None):
        super(settingDlg ,self).__init__(parent)
        self.setWindowIcon(QIcon('./icons/windowIcon.png'))
        self.height = 10
        self.width = 9
        self.size = 12
        self.cmxDir = './calibFile/calib.npz'
        label1=QLabel( self.tr("内参路径"))
        label2=QLabel( self.tr("棋盘格长（个）"))
        label3=QLabel( self.tr("棋盘格宽（个）"))
        label4=QLabel( self .tr("单格边长（毫米)"))

        self.heightLabel=QLabel("10")
        self.heightLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )
        self.widthLabel=QLabel("9")
        self.widthLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )
        self.sizeLabel=QLabel("12")
        self.sizeLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken )

        picButton=QPushButton( u"选择内参路径")
        heightButton=QPushButton( u"修改")
        widthButton=QPushButton( u"修改")
        sizeButton=QPushButton( u"修改" )
        #calibButton = QPushButton(u"开始标定")

        self.connect(picButton,SIGNAL( "clicked()"),self.slotPic)
        self.connect(heightButton,SIGNAL( "clicked()"),self.slotHeight)
        self.connect(widthButton,SIGNAL( "clicked()"),self.slotWidth)
        self.connect(sizeButton,SIGNAL( "clicked()"),self.slotSize)
        #self.connect(calibButton, SIGNAL("clicked()"), self.calib)

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
        #layout.addWidget(calibButton, 5,1, 5,2)

        self. setLayout( layout)

        self.setWindowTitle(self.tr("位姿测量设置"))

    def slotPic(self):
        img_QStringList = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./calibFile",
                                             "All Files (*);;NPZ Files (*.npz)")
        self.cmxDir = str(img_QStringList.join("<join>")).split("<join>")[0]

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
