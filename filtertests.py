from PIL import Image
import pytesseract
import argparse
import cv2
import os
imagename = "test3.png"
image = cv2.imread(imagename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#if args["preprocess"] == "thresh":
gray = cv2.threshold(gray, 120, 255,
	cv2.THRESH_BINARY)[1]
#cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]




filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename))
cleantext = text.lower().replace(' ', '_')
os.remove(filename)
print(text)
print(cleantext)

 

cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)