function [points] = generate3DChessboard (step, cell_y, cell_x, cell_size)
% step=0.5;
% cell_size = 50;
% cell_y = 7;
% cell_x = 10;

x_num = cell_x * cell_size;
y_num = cell_y * cell_size;

x_row = zeros(1, x_num);
index1 = 1;
for i = 0: x_num-1
    x_row(index1) = i*step;
    index1 = index1 + 1;
end
x = repmat(x_row, y_num, 1);

y_col = zeros(y_num,1);
index2 = 1;
for i = 0 : y_num-1
    y_col(index2) = i*step;
    index2 = index2 + 1;
end
y = repmat(y_col, 1, x_num);
z = zeros(y_num, x_num);

color1=1;
color2=color1;
color=zeros(cell_y * cell_size,cell_x * cell_size);
for i=0:(cell_y-1)
    color2=color1;
    for j=0:(cell_x-1)
        if color2==1
        color(i*cell_size+1:(i+1)*cell_size-1,j*cell_size+1:(j+1)*cell_size-1)=color2;
        end
        color2=~color2;
    end
    color1=~color1;
end
c = repmat(color(:),1, 3);
points = [x(:),y(:),z(:),c];
save('.\3DChessboard.mat', 'points');
%figure;
%scatter3(points(:,1),points(:,2),points(:,3),20,points(:,4:6),'fill');