import os
import pyautogui as pg
import time
x= 195
y=505
secret="secretpassword"
command = "application"
os.system(command)
pg.click(x, y)
pg.typewrite(secret)
pg.typewrite(["enter"])