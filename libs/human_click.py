import os
import time
import pyautogui
from pyclick import HumanClicker

BASE_DIR = os.getcwd()


def find_btn(img):
    img_path = f'targets/{img}.png'
    print(f"FIND IMG: {os.path.join(BASE_DIR, img_path)}")
    try:
        return pyautogui.center(pyautogui.locateOnScreen(os.path.join(BASE_DIR, f"targets/{img}.png"), confidence=0.7))
    except:
        print("Não encontrou nada")
        return False, False


def click_btn(button, img):
    time.sleep(.5)
    x, y = find_btn(img)
    if x and y:
        hc = HumanClicker()
        hc.move((x, y), 1.5)
        time.sleep(.5)
        hc.click()
        print(f"{button} as clicked !!!")
