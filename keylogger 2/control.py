# from pynput.mouse import Controller 
from pynput.keyboard import Controller

def controlMouse ():
    mouse = Controller()
    mouse.position = (100, 20)

def controlKeyboard ():
    Keyboard = Controller()
    Keyboard.type("I am god of this world")

# controlMouse()

controlKeyboard()

