import win32api
import win32con
import time
import math

print (time.time() * 1000)


time.sleep(5)


try:
    while True:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,10, (int)(3 * math.sin(time.time() * 25)))
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Done Farming!")