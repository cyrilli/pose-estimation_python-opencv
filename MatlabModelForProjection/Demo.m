%定义或者载入三维点阵模型，然后调用points2Image把三维模型，通过小孔相机模型来投影到二位相片中

%% generate a set of 3d points
% z = peaks;
% x = repmat(1:size(z,1),size(z,1),1);
% y = x';
% c = z - min(z(:));
% c = c./max(c(:));
% c = round(255*c) + 1;
% cmap = colormap(jet(256));
% c = cmap(c,:);
% 
% points = [x(:),y(:),z(:),c];
%% 
% Load existing 3DChessboard 
%load .\3DChessboard.mat;

% Generate 3DChessboard
points= generate3DChessboard_withWhite (0.25, 7, 10, 86);
edge = 3*0.25*86;               %计算棋盘格图案的白边边长
%% setup 

%setup camera
cam = [596.89753817,0,302.74019254,0 ;0,596.06824944,238.09315907, 0;0,0,1, 0];

%setup image
imageSize = [480,640];

%create a tform matrix
% angles = [5,-5,50]*pi/180;
% position = [-25,-25,50];
% tform = eye(4);
% tform(1:3,1:3) = angle2dcm(angles(1),angles(2),angles(3));
% tform(1:3,4) = position;

tform = [0.91967164,  0.01649788,  0.39234155,   -40.22325487;
          0.23453445,  0.77826777, -0.58248851,-73.69338177;
         -0.31495662,  0.62771578,  0.71188148,  698.67226291;
         0,0,0,1.0000];
%tform(1:2,4) = tform(1:2,4)-[edge/3*2.18;edge];
% add distortion
dist = [];

%project the points to create an image
[ image ] = points2Image(points, imageSize, cam, tform, dist, 1, 1, true);

%show the image
imshow(image);
imwrite(image, 'H:\matlab_gen_chessboard/c12.jpg')

%figure;
%scatter3(points(:,1),points(:,2),points(:,3),20,points(:,4:6),'fill');