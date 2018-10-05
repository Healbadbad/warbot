from PIL import Image
import pytesseract
import argparse
import mss
import numpy
import cv2
import os

mon = {"top": 0, "left": 0, "width": 2560, "height": 1440}
sct = mss.mss()
img = numpy.asarray(sct.grab(mon))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


### 4-part coordinates
# (140, 605) (695,655)
#  717
# 1292
# 1868
boxwidth = 555
part1 = gray[610:655, 140:140+boxwidth]
part2 = gray[610:655, 717:717+boxwidth]
part3 = gray[610:655, 1292:1292+boxwidth]
part4 = gray[610:655, 1868:1868+boxwidth]



#kinda good
#gray1 = cv2.threshold(part1, 120, 255,
#	cv2.THRESH_BINARY)[1]


#if args["preprocess"] == "thresh":
gray1 = cv2.threshold(part1, 80, 205,
	cv2.THRESH_BINARY)[1]
gray2 = cv2.threshold(part2, 80, 205,
	cv2.THRESH_BINARY)[1]
gray3 = cv2.threshold(part3, 80, 205,
	cv2.THRESH_BINARY)[1]
gray4 = cv2.threshold(part4, 80, 205,
	cv2.THRESH_BINARY)[1]
#cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


grays = [gray1, gray2, gray3, gray4]


for grayimage in grays:
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, grayimage)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	cleantext = text.lower().replace(' ', '_')
	#os.remove(filename)
	print(text)
	print(cleantext)

 

#cv2.imshow("Image", img)
#cv2.imshow("Output", gray)
cv2.imshow("gray1", gray1)
cv2.imshow("part1", part1)
cv2.imshow("part2", part2)
cv2.imshow("part3", part3)
cv2.imshow("part4", part4)
cv2.waitKey(0)