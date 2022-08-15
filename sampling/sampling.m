echo off;

I = imread('building.jpg');
I2 = im2double(I);

Filter = 1/9.*ones(3); %use lpf before down sampling
NewImage = imfilter(I2, Filter, 'replicate');
[rows,columns] = size(NewImage);

%create image with half the pixels
DownImage = NewImage(1:2:end, 1:2:end);

ZeroMatrix = reshape(1:rows*columns, rows, columns).*0;

%now add zeros to upsample again
for i=1:2:rows+1
    for j=1:2:columns+1
        ZeroMatrix(i,j) = DownImage((i+1)/2, (j+1)/2);
    end 
end

Filter2 = [0.25,0.5,0.25;0.5,1,0.5;0.25,0.5,0.25];
PaddNewImage = imfilter(ZeroMatrix, Filter2);

mse = sum(sum(power(I2-PaddNewImage,2)))/(rows*columns);

psnr = 10*log10(1/mse)


