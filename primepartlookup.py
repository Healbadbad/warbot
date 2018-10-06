from PIL import Image
import pytesseract
import argparse
import mss
import numpy
import cv2
import os
import pyautogui
from warframe_market_scraper import get_item_market_price


def pprint_stats(stats):
	pstring = ""
	pstring+= "\tavg buy: {0:.1f}".format(stats[0]) + "\n"
	pstring+= "\t stdev: {0:.1f}".format(stats[1]) + "\n"
	pstring+= "\tavg sell: {0:.1f}".format(stats[2]) + "\n"
	pstring+= "\t stdev: {0:.1f}".format(stats[3]) + "\n"
	return pstring

def print_table(itemstats):
	tablestring = ""
	tablestring += "Item Name:\t\t\t| avg buy \t| avg sell"
	tablestring += "\n"

	for item in itemstats.keys():
		tablestring += item + " \t\t| " + "{:0.2f}".format(itemstats[item][0]) + "\t\t| " + "{:0.2f}".format(itemstats[item][2]) + "\n"
	return tablestring

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
	gray1 = cv2.threshold(part1, 80, 205,
		cv2.THRESH_BINARY)[1]
	gray2 = cv2.threshold(part2, 80, 205,
		cv2.THRESH_BINARY)[1]
	gray3 = cv2.threshold(part3, 80, 205,
		cv2.THRESH_BINARY)[1]
	gray4 = cv2.threshold(part4, 80, 205,
		cv2.THRESH_BINARY)[1]
	#cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	filename = "{}-relics-gray.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	grays = [gray1, gray2, gray3, gray4]

	failures = "Failed to get item stats for: \n"
	itemstats = {}

	for grayimage in grays:
		filename = "{}.png".format(os.getpid())
		cv2.imwrite(filename, grayimage)
		if debug:
			cv2.imshow("threshold", grayimage)
			cv2.waitKey(0)
			#cv2.imshow("part", part1)

		# load the image as a PIL/Pillow image, apply OCR, and then delete
		# the temporary file
		text = pytesseract.image_to_string(Image.open(filename))
		cleantext = text.lower().replace(' ', '_')
		os.remove(filename)
		print(text)
		print(cleantext)
		try:

			#print(pprint_stats(get_item_market_price(cleantext)))
			itemstats[cleantext] = get_item_market_price(cleantext)
			#alerttext += "" + cleantext + ":\n"
			#alerttext += itemstats
			#alerttext += "\n"
		except:
			#print("Item Name:\t\t\t| avg buy | avg sell")
			failures += " - " + cleantext + "\n"

			pass
	print("\n")
	print(failures)

	stattable = print_table(itemstats)
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