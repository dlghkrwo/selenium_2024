import pyautogui
import time

#find the location of the mouse
pyautogui.position()

#move the mouse location 
pyautogui.moveTo(141, 429, 2)

#move the mouse location in time(2s)
pyautogui.moveTo(149, 429, 2)

#move the mark in current location from Y-axix in 2s
pyautogui.moveRel(0, 300, 2)

#double click
pyautogui.doubleClick()
pyautogui.click(clicks=2, interval=2)

#type -> type 'a' and enter
pyautogui.typewrite('a','enter')
#false example for typewrite
#pyautogui.typewrite('abc','enter') ->  'abc' is not exist in keyboard, only single alphabet work



