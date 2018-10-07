from pynput import keyboard
from pynput.mouse import Button, Controller
import primepartlookup
from selectorbox import WarRectSelector
import multiprocessing
import os

#p1 = 
class WarBot:
    def __init__(self,):
        self.mouse = Controller()
        self.relicOCR = primepartlookup.RelicOCR()
        self.ocrSelectorState = False
        self.selectorOverlay = None
        self.selectorOverlayThread = None

        self.killSelector = multiprocessing.Value('b', False)



    def on_press(self, key):
        try:
            #print('alphanumeric key {0} pressed'.format(
            #    key.char))
            if key.char == '\\':
                print("Exiting...")
                return False
            if key.char == '[':
                self.relicOCR.lookup_primeparts()
            if key.char == ']':
                self.relicOCR.lookup_primeparts(debug=True)
            if key.char == 'p':
                print("ocrSelectorState: " + str(self.ocrSelectorState))
                print('module name:', __name__)
                print('parent process:', os.getppid())
                print('process id:', os.getpid())
                if self.ocrSelectorState:
                    print("Supposed to kill selector")
                    self.killSelector.value = True
                    self.selectorOverlayThread.join()
                    print("after join")

                    #self.selectorOverlay = None
                    pass
                else:
                    print("starting OCR Selector")
                    self.killSelector.value = False

                    self.selectorOverlay = WarRectSelector(self.killSelector)
                    self.selectorOverlayThread = multiprocessing.Process(target=self.selectorOverlay.create_Selector, args=()) 
                    self.selectorOverlayThread.start()
                    #self.selectorOverlayThread.join()
                    print("here")

                self.ocrSelectorState = not self.ocrSelectorState



        except AttributeError:
            #print('special key {0} pressed'.format(
            #    key))
            pass

    def on_release(self, key):
        #print('{0} released'.format(
        #    key))
        #if key == keyboard.Key.esc:
            # Stop listener
        #    return False
        pass

# Collect events until released
if __name__ == '__main__':
    warbot = WarBot()

    with keyboard.Listener(
            on_press=warbot.on_press,
            on_release=warbot.on_release) as listener:
        listener.join()