import cv, cv2
import numpy as np 

def plot_circles(img_src, img_out):
	"""Finds and plots circles using Hough Circle detection."""
	circles = cv2.HoughCircles(img_src, cv2.cv.CV_HOUGH_GRADIENT, 1, img_src.shape[0]/8, param1=70, param2=40, minRadius=0, maxRadius=0)

	if circles is not None:
		print 'Circles detected'
		for c in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(img_out,(c[0],c[1]),c[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(img_out,(c[0],c[1]),2,(0,0,255),3)
	else:
		print 'No circles detected'

def color_shift(img_src):
	"""Converts video from original colorspace to isolate red objects.  Returns mask of isolated color."""
	# Convert BGR to HSV colorspace
	hsv_img = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
	# Define range of red color in HSV
	lower_red = np.array([0, 50, 50])
	upper_red = np.array([10, 255, 255])

	# Threshold HSV image to get only red colors
	mask = cv2.inRange(hsv_img, lower_red, upper_red)

	# Bitwise-AND mask and original frame -- if you want to see which bits you isolated
	# res = cv2.bitwise_and(frame, frame, mask=mask)

	return mask

cap = cv2.VideoCapture("output.avi")

while cap.isOpened():
	ret, frame = cap.read()

	# Processes video frames
	blur = cv2.medianBlur(frame, 3)
	grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

	mask = color_shift(blur)

	plot_circles(grey, frame)

	# Basic edge-finding using Canny detectionq
	edges = cv2.Canny(mask, 40, 80)	

	# Shows all of the things!
	cv2.imshow('Video', frame)
	cv2.imshow('Mask', mask)
	# cv2.imshow('Canny', edges)

	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()