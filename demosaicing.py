import cv2
import numpy as np


# list of image files
# crayons.jpg
# crayons_mosaic.bmp
# oldwell_mosaic.bmp
# oldwell.jpg
# pencils_mosaic.bmp
# pencils.jpg

# Create 3 channel image according to Bayer's pattern from single channel image
def get_bayer_pattern(img):
    rows, columns, channels = img.shape
    for y in range(rows):

        for x in range(columns):
            # print(y)
            if y % 2 == 0 and x % 2 == 0:
                # print('x:-'+str(x))
                # print('y:-'+str(y))
                img[y][x][0] = img[y][x][0]
                img[y][x][1] = 0
                img[y][x][2] = 0
                continue

            if (x + y) % 2 != 0:
                img[y][x][2] = img[y][x][0]
                img[y][x][1] = 0
                img[y][x][0] = 0
                continue

            if (x + y) % 2 == 0:
                img[y][x][1] = img[y][x][0]
                img[y][x][2] = 0
                img[y][x][0] = 0
    return img


image = cv2.imread('files/images/pencils_mosaic.bmp')
original_image = cv2.imread('files/images/pencils.jpg')

image_mosaic = get_bayer_pattern(image)

# splitting the bayer's representation of image into blue, green, red channel image

b, g, r = cv2.split(image_mosaic)

# defining the kernel for all 3 channels to find the missing information

d_depth = 0
delta = 0
anchor = (-1, -1)

blue_kernel = np.array([[0.25, 0.5, 0.25],
                        [0.5, 1, 0.5],
                        [0.25, 0.5, 0.25]])
b = cv2.filter2D(b, d_depth, blue_kernel)

green_kernel = np.array([[0.25, 0.5, 0.25],
                         [0.5, 1, 0.5],
                         [0.25, 0.5, 0.25]])
g = cv2.filter2D(g, d_depth, green_kernel)

red_kernel = np.array([[0, 0.25, 0],
                       [0.25, 1, 0.25],
                       [0, 0.25, 0]])
r = cv2.filter2D(r, d_depth, red_kernel)

image_mosaic = cv2.merge((b, g, r))

cv2.imshow('given_image', image)
cv2.waitKey(0)

cv2.imshow('original_image', original_image)
cv2.waitKey(0)

cv2.imshow('mosaic_image', image_mosaic)
cv2.waitKey(0)

difference_part_a = cv2.absdiff(image_mosaic, original_image)

cv2.imshow('difference_between_original_mosaic', difference_part_a)
cv2.waitKey(0)

# result_part_a = np.concatenate((original_image, image_mosaic, difference_part_a), axis=1)
# cv2.imshow('original_image, mosaic_image, absolute_difference', result_part_a)

# part - b
image_mosaic_improve = image_mosaic.copy()
image_mosaic_improve = image_mosaic_improve.astype(np.float32)
blue, green, red = cv2.split(image_mosaic_improve)

blue_diff = cv2.subtract(blue, red)
green_diff = cv2.subtract(green, red)

blue_blur = cv2.medianBlur(blue_diff, 3)
green_blur = cv2.medianBlur(green_diff, 3)

blue_add = blue_blur + red
green_add = green_blur + red

# To prevent overflow of pixel values
blue_add = np.where(blue_add > 255, 255, blue_add)
green_add = np.where(green_add > 255, 255, green_add)

blue_add = np.where(blue_add < 0, 0, blue_add)
green_add = np.where(green_add < 0, 0, green_add)

image_mosaic_improve = cv2.merge((blue_add, green_add, red))
image_mosaic_improve = image_mosaic_improve.astype(np.uint8)

cv2.imshow('improved_mosaic_image', image_mosaic_improve)
cv2.waitKey(0)

difference_part_b = cv2.absdiff(image_mosaic_improve, original_image)

cv2.imshow('difference_between_original_improved_mosaic', difference_part_b)
cv2.waitKey(0)

# cv2.imshow('diff', cv2.absdiff(difference_part_a, difference_part_b))
# cv2.waitKey(0)

# result_part_b = np.concatenate((original_image, image_mosaic_improve, difference_part_b), axis=1)

# final_result = np.concatenate((result_part_a, result_part_b), axis=0)
# cv2.imshow('original_image, mosaic_image, absolute_difference', final_result)
# cv2.waitKey(0)
