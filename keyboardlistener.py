from pynput import keyboard
import primepartlookup


def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(
        #    key.char))
        if key.char == '\\':
            print("Exiting...")
            return False
        if key.char == '[':
            primepartlookup.lookup_primeparts()


    except AttributeError:
        #print('special key {0} pressed'.format(
        #    key))
        pass

def on_release(key):
    #print('{0} released'.format(
    #    key))
    #if key == keyboard.Key.esc:
        # Stop listener
    #    return False
    pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()