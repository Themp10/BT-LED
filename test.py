import ctypes
import pyautogui
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
print(pyautogui.size().width)