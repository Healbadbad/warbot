import win32api
import win32con
import time

import pyautogui

time.sleep(2)

# win32api.keybd_event(ord('1'), 0, 0, 0)
# win32api.keybd_event(ord('1'), 0, win32con.KEYEVENTF_KEYUP | win32con.KEYEVENTF_EXTENDEDKEY, 0)
# time.sleep(1)


pyautogui.keyDown('w')
time.sleep(1)
pyautogui.keyUp('w')