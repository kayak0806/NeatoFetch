import cv, cv2
import numpy as np 

cap = cv2.VideoCapture("webcam_ball_test3.avi")

cv2.namedWindow('Video')
cv2.namedWindow('Blur')
# cv2.namedWindow('Canny')

while cap.isOpened():
	ret, frame = cap.read()

	# Processes video frames
	grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.medianBlur(grey, 5)

	# Attempts to find circles using Hough Transform
	circles = cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT, .5, blur.shape[0]/8, param1=100, param2=30, minRadius=0, maxRadius=0)
	if circles is not None:
		for c in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(frame,(c[0],c[1]),c[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(frame,(c[0],c[1]),2,(0,0,255),3)
	else:
		print 'No circles detected'

	# Basic edge-finding using Canny detection
	edges = cv2.Canny(blur, 40, 80)	

	# Shows all of the things!
	cv2.imshow('Video', frame)
	cv2.imshow('Blur', blur)
	# cv2.imshow('Canny', edges)

	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()