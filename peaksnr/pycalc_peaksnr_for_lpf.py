import math as m
import numpy as np
from PIL import Image


def main():
    img = Image.open("lena.gif")
    img_array = np.array(img, dtype=float)
    

    dim_filter = 3
    filter = np.full((dim_filter,dim_filter), 1/9)
    padded_array = make_padd_array(img_array, dim_filter, 'replicate')
    
    #for BW image the maximum intesity is 255, so we need to normalize the data
    #we normalize afterward because python is weird with floating stuff
    peak_snr = psnr(img_array/255, do_convolution(padded_array, filter, dim_filter)/255, 255)
    print("The peak snr value for the first filter is: ", peak_snr)
    
    
    dim_filter = 5
    filter = np.full((dim_filter,dim_filter), 1/25)
    padded_array = make_padd_array(img_array, dim_filter, 'replicate')
    
    #for BW image the maximum intesity is 255, so we need to normalize the data
    #we normalize afterward because python is weird with floating stuff
    peak_snr = psnr(img_array/255, do_convolution(padded_array, filter, dim_filter)/255, 255)
    print("The peak snr value for the second filter is: ", peak_snr)

    return 0;

def psnr(orig_array, filtered_array, peak_val):
    rows, cols = orig_array.shape
    mse = 1/(rows*cols)*np.sum((orig_array - filtered_array)**2)
    peaksnr = 10*m.log(peak_val**2/mse, 10)  
    return peaksnr;

def do_convolution(parray, filter, filter_dimension):
    rows, columns = parray.shape
    padding = m.floor(filter_dimension/2)
    rows = rows - 2*padding
    columns = columns - 2*padding
    new_array = np.full((rows, columns), 1)
    
    for i in range(0,rows):
        for j in range(0, columns):
            new_array[i, j] = np.sum(parray[i:i+filter_dimension, j:j+filter_dimension]*filter)
  
    return new_array;


def make_padd_array(array, filter_dimension, type):
    rows, columns = array.shape
    padding = m.floor(filter_dimension/2)

    padd_array = np.full((rows + 2*padding, columns + 2*padding), 0)
    padd_array[padding:-padding, padding:-padding] = array


    if type == 'replicate':
        for i in range(0,padding):
            padd_array[padding:-padding, i] = array[:, 0]
            padd_array[padding:-padding, -i-1] = array[:, -1]
            padd_array[i, padding:-padding] = array[0, :]
            padd_array[-i-1, padding:-padding] = array[-1, :]
    
        padd_array[0:padding, 0:padding] = np.full((padding, padding), array[0,0])
        padd_array[0:padding, -padding:] = np.full((padding, padding), array[0,-1])
        padd_array[-padding:, 0:padding] = np.full((padding, padding), array[-1,0])
        padd_array[-padding:, -padding:] = np.full((padding, padding), array[-1,-1])
    elif type != 'zero':
        print(f"Type \"{type}\" not defined returning zero padded array")
        
    return padd_array

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

if __name__ == "__main__":
    main()