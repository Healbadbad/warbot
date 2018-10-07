import win32api
import win32con
import time
import math

mirage_refresh_timer = 30

start_time = time.time()

time.sleep(5) # Click on Warframe game during this time

win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
win32api.keybd_event(ord('1'), 0, 0, 0)
win32api.keybd_event(ord('1'), 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(0.8)
win32api.keybd_event(ord('3'), 0, 0, 0)
win32api.keybd_event(ord('3'), 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(1)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0 ,0, 0, 0)



# TODO: Automatically find Warframe instance
try:
    while True:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,10, (int)(3 * math.sin(time.time() * 25)))
        time.sleep(0.01)

        # if time.time() > start_time + mirage_refresh_timer:
        #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        #     win32api.keybd_event(ord('1'), 0, 0, 0)
        #     time.sleep(.05)
        #     win32api.keybd_event(ord('1'), 0, win32con.KEYEVENTF_KEYUP, 0)
        #     time.sleep(0.8)
        #     win32api.keybd_event(ord('3'), 0, 0, 0)
        #     time.sleep(.05)
        #     win32api.keybd_event(ord('3'), 0, win32con.KEYEVENTF_KEYUP, 0)
        #     time.sleep(1)
        #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0 ,0, 0, 0)
        #     start_time = time.time()


except KeyboardInterrupt:
    print("Done Farming!")