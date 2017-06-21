# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2
import time
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Video import Video
from playDemoVideo import playDemoVideo
from recordVideo import recordVideo
from poseEstimate import poseEstimate
from inputDialog import InputDlg
from settingDialog import settingDlg

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MainWidget(QMainWindow):
    def __init__(self ,parent=None):
        super(MainWidget ,self).__init__(parent)
        self.raw_img = np.array([])
        self.play_flag = 0
        self.demo_path = './demoVideo/Demo.avi'
        # 设置主窗口
        self.setWindowIcon(QIcon('./icons/windowIcon.png'))
        self.showFullScreen()
        self.setWindowTitle(self.tr("位姿估计"))
        self.imageLabel=QLabel()
        #self.img = QPixmap.fromImage(QImage("640_4800.jpg"))
        #te.setPixmap(self.img)
        self.imageLabel.setMaximumSize(480, 360)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.imageLabel)

        # 设置工具栏
        self.toolbar()

        # 设置菜单栏
        self.menu()

        # 停靠窗口1
        dock1= QDockWidget(self.tr("进行位姿测量的帧"),self)
        dock1.setFeatures(QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea|Qt. RightDockWidgetArea)

        self.te1 = QLabel()
        dock1.setWidget(self.te1)
        dock1.setMaximumSize(320, 240)
        dock1.setMinimumSize(320, 240)
        self.addDockWidget(Qt.RightDockWidgetArea,dock1)

        # 停靠窗口2
        dock2=QDockWidget ( self.tr("位姿测量结果"),self)
        dock2.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget . DockWidgetClosable)
        self.te2=QTextEdit( self.tr("本窗口将显示位姿处理结果"))
        dock2.setWidget(self.te2)
        dock2.setMinimumSize(320, 240)
        self.addDockWidget(Qt.RightDockWidgetArea,dock2)
     

    def toolbar(self):
        # 定义开始，停止，估计位姿和退出，这四种动作
        quitAction = QAction(QIcon('./icons/quit.png'), u'退出', self)
        quitAction.triggered.connect(self.quit)

        startAction = QAction(QIcon('./icons/start.png'), u'开始采集', self)
        startAction.triggered.connect(self.start)

        stopAction = QAction(QIcon('./icons/stop.png'), u'停止采集', self)
        stopAction.triggered.connect(self.stop)

        estimateAction = QAction(QIcon('./icons/estimate.png'), u'估计位姿', self)
        estimateAction.triggered.connect(self.estimate)

        # 动作： 拍摄标定用的图片
        calibCaptureAction = QAction(QIcon('./icons/camera.png'), u'拍照', self)
        self.connect(calibCaptureAction, SIGNAL("triggered()"), self.calibCapture)

        # 动作： 录制视频
        recordVideoAction = QAction(QIcon('./icons/record.png'), u'录像', self)
        self.connect(recordVideoAction, SIGNAL("triggered()"), self.recordVideo)

        # 把按钮和动作连接到一起
        toolBar = self.addToolBar("开始")
        toolBar.addAction(startAction)

        toolBar = self.addToolBar("停止")
        toolBar.addAction(stopAction)

        toolBar = self.addToolBar("退出")
        toolBar.addAction(quitAction)

        toolBar = self.addToolBar("估计")
        toolBar.addAction(estimateAction)

        toolBar = self.addToolBar("拍照")
        toolBar.addAction(calibCaptureAction)
        
        toolBar = self.addToolBar("录像")
        toolBar.addAction(recordVideoAction)

    def menu(self):
        # 定义动作：
        # 动作： 标定
        calibAction = QAction(self.tr("标定相机"), self)
        calibAction.setStatusTip(self.tr("标定相机"))
        self.connect(calibAction, SIGNAL("triggered()"), self.calib_Cam)

        # 动作： 播放白天演示视频
        dayDemoAction = QAction(self.tr("演示1"), self)
        self.connect(dayDemoAction, SIGNAL("triggered()"), self.dayDemo)


        # 动作： 打开位姿测量设置窗口
        estimateSettingAction = QAction(self.tr("位姿测量设置"), self)
        self.connect(estimateSettingAction, SIGNAL("triggered()"), self.estimateSetting)

        # Action: Select demo_path
        demoPathSettingAction = QAction(self.tr("演示路径设置"), self)
        self.connect(demoPathSettingAction, SIGNAL("triggered()"), self.setDemoPath)

        
        menubar = self.menuBar()
        calibMenu = menubar.addMenu(u'&标定')
        demoMenu = menubar.addMenu(u'&演示视频')
        settingMenu = menubar.addMenu(u'&设置')
        
        calibMenu.addAction(calibAction)
        demoMenu.addAction(dayDemoAction)
        demoMenu.addAction(demoPathSettingAction)
        settingMenu.addAction( estimateSettingAction)
        
    def start(self):
        self.play_flag = 1
        self.video = Video()
        self._timer1 = QTimer(self)
        try:
            self._timer1.timeout.connect(self.play)
        finally:
            self._timer1.start(0)
            self.update()

    def play(self):
        try:
            self.video.captureRawFrame()
            self.imageLabel.setPixmap(self.video.convertFrame())

        except TypeError:
            print "No frame"

    def playAndRecord(self):
        try:
            self.rec_video.captureRawFrame()
            self.rec_video.record()
            self.imageLabel.setPixmap(self.rec_video.convertFrame())
        except TypeError:
            print "No frame"

    def stop(self):
        if self.play_flag ==1:
            self._timer1.stop()
            self.video.vs.stop()
        elif self.play_flag == 2:
            self._timer1.stop()
            self.video.capture.release()
        elif self.play_flag == 3:
            self._timer1.stop()            
            self.rec_video.vs.stop()
            self.rec_video.writer.release()
        self.play_flag = 0


    def quit(self):
        try:
            self._timer1.stop()
        finally:
            sys.exit(0)

    def estimate(self):
        img = self.video.raw_img
        try:
            chessboard_h = self.settingDialog.height
            chessboard_w = self.settingDialog.width
            chessboard_size = self.settingDialog.size
            cmxDir = self.settingDialog.cmxDir
        except:
            self.settingDialog = settingDlg()
            self.settingDialog.show()
        pos = poseEstimate(img,chessboard_h, chessboard_w, chessboard_size, cmxDir)
        img = pos.solvePnP()

        # Save result to txt file in experiment_data
        self.saveData('test',pos.rvec_str,pos.tvec_str, pos.err_str)
        
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width = img.shape[:2]
            img = QImage(img,
                               width,
                               height,
                               QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
        except:
            return None
        img = img.scaledToHeight(320)
        img = img.scaledToWidth(240)
        self.te1.setPixmap(img)
        if pos.ret ==1:
            self.te2.setText(self.tr("旋转向量为："))
            #self.te2.append('')
            self.te2.append(pos.rvec_str)
            
            self.te2.append(self.tr("平移向量为："))
            #self.te2.append('')
            self.te2.append(pos.tvec_str)
            self.te2.append('')
            self.te2.append(self.tr("重投影误差是：")+pos.err_str)
        else:
            self.te2.setText(self.tr("No Chessboard!"))

    def calib_Cam(self):
        '''
        打开标定对话框，并输入相关参数进行标定，标定结果被保存在./calibFile/calib.npz
        '''
        self.inputDialog = InputDlg()
        self.inputDialog.show()

    def calibCapture(self):
        '''
        每隔3秒拍摄一张照片，并保存在一个单独的文件夹中，一共拍摄15张
        与此同时用户应该手持标定板，不断摆出不同的位置和角度让相机拍摄。
        最后程序还应该输出一个包含了图片路径的list，用于calib_Cam的标定
        '''
        img = self.video.raw_img
        cv2.imwrite('./calibFile/calibImages/'+str(int(time.time()))+'.jpg', img)
        
    def recordVideo(self):
        self.play_flag = 3
        self.rec_video = recordVideo()
        self.rec_video.initRecord()
        self._timer1 = QTimer(self)
        try:
            self._timer1.timeout.connect(self.playAndRecord)
        finally:
            self._timer1.start(100)
            self.update()
    
    
    def dayDemo(self):
        '''
        播放提前录制好的白天标定板不断运动的图像
        '''
        self.startDemo(self.demo_path)

    def nightDemo(self):
        '''
        播放提前录制好的夜间标定板不断运动的视频
        '''
        pass

    def startDemo(self,file):
        self.play_flag = 2
        self.video = playDemoVideo(file)
        self._timer1 = QTimer(self)
        try:
            self._timer1.timeout.connect(self.play)
        finally:
            self._timer1.start(100)
            self.update()
            
    def saveData(self,experiment_name,rvec, tvec, error):
        f = open('./experiment_data/'+str(experiment_name)+'.txt','a')
        f.writelines(rvec+","+tvec+","+error+'\n')
        f.close()
    
    def estimateSetting(self):
        self.settingDialog=settingDlg()
        self.settingDialog.show()

    def setDemoPath(self):
        demo_QStringList = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./demoVideo",
                                             "All Files (*);;AVI Files (*.avi)")
        self.demo_path = str(demo_QStringList.join("<join>")).split("<join>")[0]

        
app=QApplication (sys.argv)
main=MainWidget()
main. show ()
app.exec_()
