echo off;

I = imread('lena.gif');
% I = imread('railroad.jpg')
% I = imread('wolfy.jpg');
I2 = im2double(I);


% Filter = 1/9.*ones(3);
Filter = [[-1 -1 -1]; [-1 9 -1]; [-1 -1 -1]] %hpf test
NewImage = imfilter(I2, Filter, 'replicate');
imwrite(NewImage, 'processed_lena.png');

%Computing the peaksnr value assumeing the the maximum is 255 (8-bit b/w image)
mse = 1/(256*256)*sum( (I2 - NewImage).^2, 'all')
peaksnr = 10*log10(255^2/mse);
[pksnr, snr] = psnr(NewImage, I2, 255); 
fprintf('\n The Peak-SNR value is %0.4f\n', pksnr);



Filter = 1/25.*ones(5);
NewImage2 = imfilter(I2, Filter, 'replicate');
imwrite(NewImage, 'processed_lena2.png');

%Computing the peaksnr value assumeing the the maximum is 255 (8-bit b/w image)
mse2 = 1/(256*256)*sum( (I2 - NewImage2).^2, 'all');
peaksnr2 = 10*log10(255^2/mse2);
[pksnr2, snr2] = psnr(NewImage2, I2, 255);
fprintf('\n The Peak-SNR value is %0.4f\n', pksnr2);
