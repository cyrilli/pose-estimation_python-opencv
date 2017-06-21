function [ image ] = points2Image( points, imageSize, cam, tform, D, pointRadius, opacity, useMex )
%POINTS2IMAGE Uses a camera model to project 3D points onto a plane to 
%   Required Inputs:
%   points- nxm set of 3d points, the 1st 3 columns are the point locations
%   (x,y,z) and the remaining coloumns the intensity values (i1,i2,etc), if
%   no intensity values are given, all points will have an intensity of 1
%   imageSize- 1x2 vector giving the height and width of the output image 
%   [h,w]
%   cam- either a 3x4 camera projection matrix or a scalar focal length
%
%   Optional Inputs: (will give default values on empty array [])
%   tform- 4x4 transform to apply to points before projecting them (default
%   identity matrix)
%   pointRadius- radius of point in pixels (default 1)
%   opacity- scalar with range 0 to 1, specifies opacity of points (default
%   1)
%   useMex- use a mex file to speed up process (default true)
%
%   Outputs:
%   image- hxwx(m-3) output image of given size with (m-3) colour bands

%% check inputs

validateattributes(points, {'numeric'},{'2d'});
if(size(points,2) < 3)
    error('points must have atleast 3 columns, currently has %i',size(points,2));
end
validateattributes(imageSize, {'numeric'},{'size',[1,2],'positive','integer'});

if(size(cam,2) == 3)
    cam(end,4) = 0;
end
validateattributes(cam, {'numeric'},{'size',[3,4]});

if(nargin < 4)
    tform = [];
end
if(isempty(tform))
    tform = eye(4);
else
    validateattributes(tform, {'numeric'},{'size',[4,4]});
end

if(nargin < 5)
    D = [];
end
if(isempty(D))
    D = [0,0,0,0,0];
else
    validateattributes(D, {'numeric'},{'nrows',1});
end
if(size(D,2) > 5)
    error('distortion vector D, must have 5 or less columns currently has %i',size(D,2));
end
D = double(D);

if(nargin < 6)
    pointRadius = [];
end
if(isempty(pointRadius))
    pointRadius = 1;
else
    validateattributes(pointRadius, {'numeric'},{'scalar','positive','integer'});
end

if(nargin < 7)
    opacity = [];
end
if(isempty(opacity))
    opacity = 1;
else
    validateattributes(opacity, {'numeric'},{'scalar','positive'});
    if((opacity > 1) || (opacity < 0))
        error('Opacity must be in range 0 to 1');
    end
end

if(nargin < 8)
    useMex = [];
end
if(isempty(useMex))
    useMex = true;
else
    validateattributes(useMex, {'logical'},{'scalar'});
end

%convert elements which require precision to doubles
points = double(points);
tform = double(tform);
cam = double(cam);

%% run image generation

%create filter
disk = fspecial('disk',pointRadius);
disk = opacity.*disk./max(disk(:));

%split distortion into radial and tangential
if(size(D,2) < 5)
    D(1,5) = 0;
end
k = [D(1),D(2),D(5)];
p = [D(3),D(4)];

%split points into locations and colour
locs = [points(:,1:3), ones(size(points,1),1)];
if(size(points,2) > 3)
    colours = points(:,4:end);
else
    colours = ones(size(points,1),1);
end

%move camera position
locs = (tform*locs')';

%sort points by distance from camera
dist = sum(locs(:,1:3).^2,2);
[~,idx] = sort(dist,'descend');
locs = locs(idx,:);
colours = colours(idx,:);

%% Distort
%reject points behind camera
valid = locs(:,3) > 0;
locs = locs(valid,:);
colours = colours(valid,:);

%project onto a plane using normalized image coordinates
x = locs(:,1)./locs(:,3);
y = locs(:,2)./locs(:,3);

%find radial distance
r2 = x.^2 + y.^2;

%find tangential distortion
xTD = 2*p(1)*x.*y + p(2).*(r2 + 2*x.^2);
yTD = p(1)*(r2 + 2*y.^2) + 2*p(2)*x.*y;

%find radial distortion
xRD = x.*(1 + k(1)*r2 + k(2)*r2.^2 + k(3)*r2.^3); 
yRD = y.*(1 + k(1)*r2 + k(2)*r2.^2 + k(3)*r2.^3); 

%combine distorted points
x = xRD + xTD;
y = yRD + yTD;

%project distorted points back into 3D
locs = [x,y,ones(size(x,1),1)].*repmat(locs(:,3),1,3);
locs = [locs, ones(size(locs,1),1)];
%%
%project points into 2D
locs = (cam*locs')';
keep = locs(:,3) > 0;
locs = locs(keep,:);
colours = colours(keep,:);
locs = locs(:,1:2)./repmat(locs(:,3),1,2);
locs = round(locs);

%remove unseen points
keep = (locs(:,1) >= -size(disk,1)) & ...
    (locs(:,1) < (imageSize(2) + size(disk,1))) & ...
    (locs(:,2) >= -size(disk,2)) & ...
    (locs(:,2) < (imageSize(1) + size(disk,2)));

locs = locs(keep,:);
colours = colours(keep,:);
% disp(size(locs))
% disp(size(colours))
%form image
if(useMex)
    %compile if required
    if(exist('colourImage') ~= 3)
        mex colourImage.cpp;
    end
    image = colourImage(locs, colours, disk, uint32(imageSize));
else
    %run slow non-mex version of code
    image = zeros([imageSize,size(colours,2)]);
    for i = 1:size(locs,1)
       for iy = -pointRadius:pointRadius
           for ix = -pointRadius:pointRadius
               valid = (locs(i,1)+ix >= 0) & ...
                (locs(i,1)+ix < imageSize(2)) & ...
                (locs(i,2)+iy >= 0) & ...
                (locs(i,2)+iy < imageSize(1));

                if(valid)
                    opac = disk(iy+pointRadius+1,ix+pointRadius+1);
                    col = (1-opac)*image(locs(i,2)+iy+1, locs(i,1)+ix+1,:);
                    image(locs(i,2)+iy+1, locs(i,1)+ix+1,:) = col(:)' + opac*colours(i,:);
                end
           end
       end
    end
end

end