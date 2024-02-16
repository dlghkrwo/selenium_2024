import pyautogui

#find the position first
print(pyautogui.positon())

# pyautogui.moveTo(190, 159)
# pyautogui.click(190,159)

# take the screenShot
# screenShot = pyautogui.locateCenterOnScreen('7.png')
# print(screenShot)

pyautogui.screenshot('1.png', region=(1324, 789, 30, 30))
num1 = pyautogui.locateCenterOnScreen('1.png')
pyautogui.click(num1)




