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

        self.toDie = multiprocessing.Value('b', False)
        self.selectorActive = multiprocessing.Value('b', False)
        self.selectorCoordinates = multiprocessing.Array('i', range(4))

        print("starting OCR Selector")
        self.selectorActive.value = False
        self.selectorOverlay = WarRectSelector(self.toDie, self.selectorActive, self.selectorCoordinates)
        self.selectorOverlayThread = multiprocessing.Process(target=self.selectorOverlay.create_Selector, args=()) 
        self.selectorOverlayThread.start() 


    def on_press(self, key):
        try:
            #print('alphanumeric key {0} pressed'.format(
            #    key.char))
            if key.char == '\\':
                self.toDie.value = True
                self.selectorOverlayThread.join()
                print("Exiting...")
                return False
            if key.char == '[':
                self.relicOCR.lookup_primeparts()
            if key.char == ']':
                self.relicOCR.lookup_primeparts(debug=True)
            if key.char == '\'':
                #print("ocrSelectorState: " + str(self.ocrSelectorState))
                if self.ocrSelectorState:
                    self.selectorActive.value = False
                    #self.selectorOverlayThread.join()
                    #print("selector coordinates:")
                    #print(self.selectorCoordinates[:])
                    self.relicOCR.lookup_by_coordinates(self.selectorCoordinates)

                else:
                    print("starting OCR Selector")
                    self.selectorActive.value = True
                    #self.selectorOverlay = WarRectSelector(self.killSelector, self.selectorCoordinates)
                    #self.selectorOverlayThread = multiprocessing.Process(target=self.selectorOverlay.create_Selector, args=()) 
                    #self.selectorOverlayThread.start()

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