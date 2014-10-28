import cv, cv2
import numpy as np 

circle_location = []

def plot_circles(img_src, img_out):
	"""Finds and plots circles using Hough Circle detection."""
	circles = cv2.HoughCircles(img_src, cv2.cv.CV_HOUGH_GRADIENT, 1, img_src.shape[0]/8, param1=10, param2=20, minRadius=20, maxRadius=30)

	if circles is not None:
		print 'Circles detected'
		for c in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(img_out,(c[0],c[1]),c[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(img_out,(c[0],c[1]),2,(0,0,255),3)
		    global circle_location
		    circle_location.append((c[0], c[1]))

def color_shift(img_src):
	"""Converts video from original colorspace to isolate red objects.  Returns mask of isolated color."""
	# Convert BGR to HSV colorspace
	hsv_img = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
	# Define range of red color in HSV
	lower_red = np.array([0, 0, 0])
	upper_red = np.array([179, 50, 50])

	# Threshold HSV image to get only red colors
	mask = cv2.inRange(hsv_img, lower_red, upper_red)

	# Bitwise-AND mask and original frame -- if you want to see which bits you isolated
	# res = cv2.bitwise_and(frame, frame, mask=mask)

	return mask

cap = cv2.VideoCapture("output.avi")
count = 0
while cap.isOpened():
	ret, frame = cap.read()

	# Processes video frames
	blur = cv2.medianBlur(frame, 3)
	grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

	mask = color_shift(blur)

	plot_circles(mask, frame)

	# Basic edge-finding using Canny detectionq
	edges = cv2.Canny(mask, 60, 80)	

	# Shows all of the things!
	cv2.imshow('Video', frame)
	cv2.imshow('Mask', mask)
	# cv2.imshow('Canny', edges)

	if cv2.waitKey(50) & 0xFF == ord('q'):
		break

if cv2.waitKey(50) & 0xFF == ord('q'):
	cap.release()
	cv2.destroyAllWindows()

xlength, ylength = grey.shape
path = np.zeros((xlength, ylength, 3), np.uint8)
for coor in circle_location:
	cv2.circle(path,(coor), 5, (0,0,255), -1)

cv2.imshow('path', path)
k = cv2.waitKey(0) & 0xFF
if k == 27:
	cv2.destroyAllWindows()


