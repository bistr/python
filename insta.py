from pyautogui import *
from random import randint
from time import sleep

FAILSAFE = True
picsToLike=randint(25,40)
print (picsToLike)

sleep(5)
for i in range(picsToLike):
	offsetX=randint(-30,30)
	offsetY=randint(-30,30)
	sleep(0.5)
	doubleClick(400+offsetX,600+offsetY)
	sleep(0.5)
	press("right")