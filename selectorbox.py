import tkinter
import win32api, win32con, win32gui, pywintypes
import time
from pynput.mouse import Button, Controller
import multiprocessing


class WarRectSelector:

	def __init__(self, toDie, selectorActive, selectorCoordinates):
		#print("Instantiating WarRectSelector")
		self.toDie = toDie
		self.selectorActive = selectorActive
		self.prevActiveState = False
		self.selectorCoordinates = selectorCoordinates

	def create_Selector(self):
		#print("create WarRectSelector")
		self.root = tkinter.Tk()
		self.mouse = Controller()
		self.rectcoords = [self.mouse.position[0], self.mouse.position[1], 100,100]

		self.canvas = tkinter.Canvas(self.root, width=2560, height=1440, highlightthickness=0)
		self.canvas.configure(background='white')
		self.root.configure(background='white')
		self.a = self.canvas.create_rectangle(0, 0, 100, 100, outline='red')# fill='red')
		#canvas.master.attributes("-alpha", .30)
		self.canvas.pack()
		self.canvas.master.overrideredirect(True)
		#canvas.master.geometry("+250+250")
		self.canvas.master.lift()
		self.canvas.master.wm_attributes("-topmost", True)
		self.canvas.master.wm_attributes("-disabled", True)
		self.canvas.master.wm_attributes("-transparentcolor", "white")


		hWindow = pywintypes.HANDLE(int(self.root.frame(), 16))
		# http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
		# The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
		#exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
		exStyle =  win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
		win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

		#label.pack()
		#label.mainloop()
		self.canvas.pack()
		#root.mainloop()
		self.draw()
		while True:
			self.root.update_idletasks()
			self.root.update()
			if self.toDie.value:
				print("Selector Returning")
				self.root.destroy()
				exit()
		    #time.sleep(1)

	def draw(self):
		#self.canvas.pack()
		#self.canvas.update()

		if self.prevActiveState != self.selectorActive.value:
			if self.prevActiveState:
				# End selection, nothing to be done
				pass
			else:
				# start selection
				self.rectcoords[0] = self.mouse.position[0]
				self.rectcoords[1] = self.mouse.position[1]
			self.prevActiveState = self.selectorActive.value
		if self.selectorActive.value:
			self.rectcoords[2] = self.mouse.position[0]
			self.rectcoords[3] = self.mouse.position[1]
			self.selectorCoordinates[0] = self.rectcoords[0]
			self.selectorCoordinates[1] = self.rectcoords[1]
			self.selectorCoordinates[2] = self.rectcoords[2]
			self.selectorCoordinates[3] = self.rectcoords[3]
			self.canvas.coords(self.a, self.rectcoords)
		else:
			self.canvas.coords(self.a, [0, 0, 0, 0])
		
		self.canvas.after(1, self.draw)

class BasicCanvas:
	def __init__(self):
		self.root = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.root, width=500, height=500)
		self.a = self.canvas.create_rectangle(0, 0, 100, 100, fill='red')

		self.canvas.master.wm_attributes("-transparentcolor", "white")
		self.canvas.master.wm_attributes("-topmost", True)

		#canvas.master.overrideredirect(True)

		self.canvas.pack()

		hWindow = pywintypes.HANDLE(int(self.canvas.master.frame(), 16))
		# http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
		# The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
		exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
		win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

	def draw(self):
		self.canvas.pack()
		self.canvas.update()
		self.canvas.after(1, self.draw)
		#root.mainloop()

if __name__ == "__main__":
	selector = WarRectSelector(False)
	selector.create_Selector()
	#selector=BasicCanvas()
	#selector.draw()
	#selector.root.mainloop()