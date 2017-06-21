# pose-estimation_python-opencv
Camera calibration and pose estimation of a chessboard using solvePnP
Using Opencv-python to estimate pose of a chessboard.
Run camcalib.py first to calibrate the camera and get the camera matrix and distortion coefficient.
Then run solpnp.py to estimate the extrinsic matrix.

### "PoseEstimateOnRaspberryPi" 
This folder contains the program I used to run on Raspberry pi. PyQt is used to make the GUI. Run main.py

#### Required packages include:
1. PyQt4
2. OpenCV3
3. imutils（for the raspberry pi camera）
4. numpy
#### The GUI on Raspberry Pi
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/GUI.png?raw=true" width = "600" height = "400" alt="图片名称" align=center />

#### Pi NoIR infrared camera
<img src="https://github.com/cyrilli/pose-estimation_python-opencv/blob/master/img/work.jpg?raw=true" width = "600" height = "400" alt="图片名称" align=center />

### "MatlabModelForProjection" 
This folder contains a matlab model of the camera. You can specify the parameters of the intrinsic and extrinsic matrix and watch how the image of the chessboard changes.
