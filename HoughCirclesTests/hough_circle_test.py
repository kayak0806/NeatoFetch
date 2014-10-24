import cv2
import cv2.cv as cv 
import numpy as np 

# cap = cv2.videoCapture()
filename = raw_input('Enter image filename (including extension): ')
img = cv2.imread(filename) # loads image in color
img = cv2.medianBlur(img,5)	# Blurs image to reduce noise and reduce false positives
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale

# Applies Hough Circle Transform to greyscale image -- (greyscale input image, detection method, 1/resolution, min distance between detected centers, param1 = upper threshold for Canny edge detector, param2 = accumulator threshold for circle detection)
circles = cv2.HoughCircles(grey_img, cv.CV_HOUGH_GRADIENT, 1, 100, param1=60, param2=30, minRadius=0, maxRadius=0) 

# print circles

# circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

print('\nPress "Esc" to close image.  Press "s" to save.\n')

cv2.imshow('detected circles',img)

k = cv2.waitKey(0) & 0xFF
if k==27:
	cv2.destroyAllWindows()
elif k==ord('s'):
	# Save an image
	save_name = raw_input('File save name (including extension): ')
	print('Image saved')
	cv2.imwrite(save_name, img)

