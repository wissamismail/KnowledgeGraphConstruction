import sys
sys.path.append(r'C:\Users\Lym\Documents\GitHub\Selenium-python')
from time import sleep

from v2.seleniumFunctions import seleniumFunctions


seleniumFunctions.browseSauceDemo()
seleniumFunctions.safe_clicker('//input[@id="user-name"]', 1, 30, "eyyub")
sleep(10)