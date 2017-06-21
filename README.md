# pose-estimation_python-opencv
Camera calibration and pose estimation of a chessboard using solvePnP
Using Opencv-python to estimate pose of a chessboard.
Run camcalib.py first to calibrate the camera and get the camera matrix and distortion coefficient.
Then run solpnp.py to estimate the extrinsic matrix.

### 1. PoseEstimateOnRaspberryPi
This folder contains the program I used to run on Raspberry pi. PyQt is used to make the GUI. Run main.py

Required packages include:
1. PyQt4
2. OpenCV3
3. imutils（for the raspberry pi camera）
4. numpy
#### 1.1 The GUI on Raspberry Pi
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/GUI.png?raw=true" width = "600" height = "400" alt="图片名称" align=center />

#### 1.2 Pi NoIR infrared camera
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/work.jpg?raw=true" width = "600" height = "400" alt="图片名称" align=center />

### 2. MatlabModelForProjection
This folder contains a matlab model of the camera. You can specify the parameters of the intrinsic and extrinsic matrix and watch how the image of the chessboard changes.
#### 2.1 The model of chessboard made up of 3D points
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/chessboard_1.jpg?raw=true" width = "600" height = "400" alt="图片名称" align=center />

#### 2.2 The projected 2D image with user-specified parameters
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/chessboard_2.jpg?raw=true" width = "600" height = "400" alt="图片名称" align=center />
