# demosaicing_image
This is a simple application that converts an image represented in Bayers pixel pattern into a RGB representation. 

The important thing about this application is comming up with kernels(using linear interpolation - averaging 4 nearest neighbours) for each channel 
(i.e Blue, Green, Red) and using these kernels to interpolate the missing values in the channels of the image.
