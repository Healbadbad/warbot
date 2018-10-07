from PIL import Image
import pytesseract
import argparse
import mss
import numpy as np
import cv2
import os
import pyautogui
from warframe_market_scraper import get_item_market_price
from warframe_market_scraper import get_item_ducats
from warframe_item import WarframeItem
from warframe_item_printer import WarframeItemPrinter

class RelicOCR:

	def __init__(self):
		# Tesseract Config
		# https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
		self.tesseract_config = r'--psm 3' 
		self.mon = {"top": 0, "left": 0, "width": 2560, "height": 1440}

	def preprocess_image_slice(self, grayimage, invert=True):
		img = grayimage
		#img = cv2.resize(grayimage, None, fx=0.75, fy=0.75, interpolation=cv2.INTER_CUBIC)
		kernel = np.ones((1, 1), np.uint8)
		img = cv2.dilate(img, kernel, iterations=1)
		img = cv2.erode(img, kernel, iterations=1)
		img = cv2.GaussianBlur(img, (3, 3), 0)
		if invert:
			img = cv2.threshold(img, 80, 205, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
			img = 255 - img
		else:
			img = cv2.threshold(img, 80, 125, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

		return img

	def lookup_by_coordinates(self, coordinates, debug=False):
		sct = mss.mss()
		width = coordinates[2] -coordinates[0]
		height = coordinates[3] - coordinates[1]
		if width < 0 or height < 0:
			print("Draw a better box")
			return
		mon = {"top": coordinates[1],
			 "left": coordinates[0],
			 "width": width,
			 "height": height}

		img = np.asarray(sct.grab(mon))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		parts = [gray]

		self.process_image_parts(parts, debug=debug)


	def lookup_primeparts(self, count=4, debug=False):
		sct = mss.mss()
		img = np.asarray(sct.grab(self.mon))
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

		parts = [part1, part2, part3, part4]

		self.process_image_parts(parts, debug=debug)

	def process_image_parts(self, parts, debug=False):
		thresholded = []
		for part in parts:
			thresholded.append(self.preprocess_image_slice(part))

		failures = "Failed to get item stats for: \n"
		items = []
		debugimages = []

		for grayimage in thresholded:
			itemstring = pytesseract.image_to_string(grayimage, lang='eng', config=self.tesseract_config)
			print(itemstring)

			if debug:
				continue
			try:
				items.append(WarframeItem(itemstring))
			except:# Exception as e:
				failures += " - " + itemstring + "\n"
				pass
				#print(e.what)

		print("\n")
		print(failures)

		printer = WarframeItemPrinter(items)
		printer.tabulate()

		if debug:
			        # Create a named window
			for i in range(len(thresholded)):
				winname = "threshold " + str(i)
				cv2.namedWindow(winname)
				cv2.imshow(winname, thresholded[i])
				cv2.moveWindow(winname, -700, 150 + i*90)

			cv2.waitKey(1)

if __name__ == "__main__()":
	lookup_primeparts()
