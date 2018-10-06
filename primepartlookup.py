from PIL import Image
import pytesseract
import argparse
import mss
import numpy
import cv2
import os
import pyautogui
from warframe_market_scraper import get_item_market_price
from warframe_market_scraper import get_item_ducats

def pprint_stats(stats):
	pstring = ""
	pstring+= "\tavg buy: {0:.1f}".format(stats[0]) + "\n"
	pstring+= "\t stdev: {0:.1f}".format(stats[1]) + "\n"
	pstring+= "\tavg sell: {0:.1f}".format(stats[2]) + "\n"
	pstring+= "\t stdev: {0:.1f}".format(stats[3]) + "\n"
	return pstring

def print_table(itemstats, ducats):
	tablestring = ""
	tablestring += "Item Name:\t\t\t| avg buy \t| avg sell \t| ducats "
	tablestring += "\n"

	for item in itemstats.keys():
		tablestring += item + " \t\t| " + "{:0.2f}".format(itemstats[item][0]) + "\t\t| " + "{:0.2f}".format(itemstats[item][2]) + "\t\t| " + str(ducats[item]) + "\n"
	return tablestring

def clean_item_name(dirtytext):
	# lowercase
	# check for chassis, neuroptics, systems
	# if true, remove blueprint from end
	# replace space
	temptext = dirtytext.lower()
	words = temptext.split(' ')
	for word in ["chassis", "neuroptics", "systems"]:
		if word in words and "blueprint" in words:
			words = words[:-1]
			break

	cleanName = ""
	for word in words:
		cleanName += word + "_"
	cleanName = cleanName[:-1]
	return cleanName

def preprocess_blobs(image):
	
	kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
	thresholded.append(cv2.threshold(part, 80, 205,
		cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])

def lookup_primeparts(count=4, debug=False):
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
	parts = [part1, part2, part3, part4]
	thresholded = []
	for part in parts:

	#cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	filename = "{}-relics-gray.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	#grays = [gray1, gray2, gray3, gray4]

	failures = "Failed to get item stats for: \n"
	itemstats = {}
	ducats = {}

	for grayimage in thresholded:
		if debug:
			cv2.imshow("threshold", grayimage)
			cv2.waitKey(0)
			#cv2.imshow("part", part1)

		# Tesseract Config
		# https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
		tesseract_config = r'--psm 3 --oem 1' 
		text = pytesseract.image_to_string(grayimage, lang='eng', config=tesseract_config)
		cleantext = clean_item_name(text)
		print(text)
		print(cleantext)
		if debug:
			continue
		try:

			#print(pprint_stats(get_item_market_price(cleantext)))
			itemstats[cleantext] = get_item_market_price(cleantext)
			ducats[cleantext] = get_item_ducats(cleantext)
			#alerttext += "" + cleantext + ":\n"
			#alerttext += itemstats
			#alerttext += "\n"
		except:# Exception as e:
			#print(e.what)
			#print("Item Name:\t\t\t| avg buy | avg sell")
			failures += " - " + cleantext + "\n"

			pass
	print("\n")
	print(failures)

	stattable = print_table(itemstats, ducats)
	print(stattable)



	#pyautogui.alert(text=alerttext, title="Prime part Prices", button='OK')
 
if __name__ == "__main__()":
	lookup_primeparts()

#cv2.imshow("Image", img)
#cv2.imshow("Output", gray)

#cv2.imshow("part2", part2)
#cv2.imshow("part3", part3)
#cv2.imshow("part4", part4)
#cv2.waitKey(0)