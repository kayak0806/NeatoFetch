#!/usr/bin/env python

import cv2
cv2.namedWindow("ImageWindow", 1)
img=cv2.imread('/home/kgallagher/Pictures/peek_owl.jpg')
cv2.imshow('ImageWindow',img)
cv2.waitKey(0)
cv2.imwrite('/home/kgallagher/Pictures/peek_owl2.jpg',img)