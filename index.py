# -*- coding: utf-8 -*-
import json
import os
import sys
import mss
import time
import sys
import yaml
import numpy as np
import pyautogui
import platform
import subprocess
import webbrowser
from sys import platform as sys_platform
from src.logger import logger, loggerMapClicked
from cv2 import cv2
from os import listdir, getcwd, path, environ, popen
from random import randint
from random import random

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
ch = c['home']
multiple_tabs = c["multiple_tabs"]
pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause
BASE_DIR = getcwd()

cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0x1305EE0e2a22070EfB7aF35e567f7Fa370D5F302 ===============
=========================================================================
===== https://nubank.com.br/pagar/1nb7na/SvujVdhX49 ======
=========================================================================

>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be found in the config.yaml file."""


def get_platform():
    if sys_platform in ('win32', 'cygwin'):
        import pygetwindow
        return 'Windows'
    elif sys_platform == 'darwin':
        return 'Macosx'
    elif sys_platform.startswith('linux'):
        import Xlib.display
        from pyvirtualdisplay import Display
        if platform.node() == 'raspberrypi':
            return 'Raspberrypi'
        return 'Linux'
    elif sys_platform.startswith('freebsd'):
        return 'Linux'
    return 'Unknown'


def run_command(command):
    try:
        result = subprocess.check_output(command).decode("utf-8")
    except:
        result = [os.popen(command[0]).read()]
    return result


def get_windows_with_title(title):
    # sudo apt-get install xdotool wmctrl
    windows_list = [w.split() for w in run_command(["wmctrl", "-lG"]).splitlines()]
    # check if the window is "normal" and / or minimized
    windows_with_title = [
        {"id": w[0], "is_minimized": all([
            "_NET_WM_STATE_HIDDEN" not in run_command(["xprop", "-id", w[0]]),
            "_NET_WM_WINDOW_TYPE_NORMAL" in run_command(["xprop", "-id", w[0]])]),
         "application": " ".join(w[-2:]).replace("–", "").lstrip(), "title": w[7]
         } for w in windows_list if title in w[7]]

    return windows_with_title


def run_chrome():
    global images

    width, height = pyautogui.size()

    # v_display = Display(visible=True, size=(width, height))
    # v_display.start()
    # pyautogui._pyautogui_x11._display = Xlib.display.Display(environ['DISPLAY'])

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--profile-directory=Profile 4")
    options.add_argument("user-data-dir=/home/cleiton/.config/google-chrome/")
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    # ac = ActionChains(driver)

    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    # driver.set_window_size(width, height)

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(c["password"])

    xpaths = ['//*[@id="app-content"]/div/div[4]/div/div/button/span',
              '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]',
              '//*[@id="app-content"]/div/div[3]/div/div/button',
              '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]']

    success_click = False

    for xpath in xpaths:
        success_click = click_xpath_button(driver, xpath)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://app.bombcrypto.io/webgl/index.html')

    time.sleep(5)

    buttons = ["wallet", "connect-wallet", "connect", "select-wallet-2", "confirm"]
    for button in buttons:
        success_click = click_img_button(f"targets/{button}.png")
        time.sleep(2)

    if not success_click:
        sys.exit(0)

    # driver.set_window_size(1040, 900)
    main()


def click_xpath_button(driver, xpath, delay=3):
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).click()
    except TimeoutException:
        print("Loading took too much time!")
    return True


def click_img_button(img_path):
    button = pyautogui.locateOnScreen(path.join(BASE_DIR, img_path), grayscale=True, confidence=0.5)
    if button:
        pyautogui.moveTo(button, duration=.1)
        pyautogui.click(button, clicks=2, interval=2)
        return True
    return False


def addRandomness(n, randomn_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        randomn_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)


def moveToWithRandomness(x, y, t):
    pyautogui.moveTo(addRandomness(x, 10), addRandomness(y, 10), t + random() / 2)


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def load_images(dir_path='./targets/'):
    """ Programatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    time.sleep(2)
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def loadHeroesToSendHome():
    """Loads the images in the path and saves them as a list"""
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes


def show(rectangles, img=None):
    """ Show an popup with rectangles showing the rectangles[(x, y, w, h),...]
        over img or a printSreen if no img provided. Useful for debugging"""

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255, 255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)


def clickBtn(img, timeout=3, threshold=ct['default']):
    """Search for img in the scree, if found moves the cursor over it and clicks.
    Parameters:
        img: The image that will be used as an template to find where to click.
        timeout (int): Time in seconds that it will keep looking for the img before returning with fail
        threshold(float): How confident the bot needs to be to click the buttons (values from 0 to 1)
    """

    logger(None, progress_indicator=True)
    start = time.time()
    has_timed_out = False
    while not has_timed_out:
        matches = positions(img, threshold=threshold)

        if len(matches) == 0:
            has_timed_out = time.time() - start > timeout
            continue

        x, y, w, h = matches[0]
        pos_click_x = x + w / 2
        pos_click_y = y + h / 2
        moveToWithRandomness(pos_click_x, pos_click_y, 1)
        pyautogui.click()
        return True

    return False


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def positions(target, threshold=ct['default'], img=None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def scroll():
    """
    commoms = positions(images['commom-text'], threshold = ct['commom'])
    if (len(commoms) == 0):
        commoms = positions(images['rare-text'], threshold = ct['rare'])
        if (len(commoms) == 0):
            commoms = positions(images['super_rare-text'], threshold = ct['super_rare'])
            if (len(commoms) == 0):
                commoms = positions(images['epic-text'], threshold = ct['epic'])
                if (len(commoms) == 0):
                    return
    x,y,w,h = commoms[len(commoms)-1]
    moveToWithRandomness(x,y,1)
    """
    commoms = positions(images['commom-text'], threshold=ct['commom'])
    if len(commoms) == 0:
        return
    x, y, w, h = commoms[len(commoms) - 1]
    #
    moveToWithRandomness(x, y, 1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0, -c['click_and_drag_amount'],
                          duration=1, button='left')


def clickButtons():
    time.sleep(2)
    all_go_work_button = False
    if pyautogui.locateOnScreen(images["all-go-work"]):
        buttons = positions(images['all-go-work'], threshold=ct['all_go_to_work_btn'])
        logger('All button found, click!')
        all_go_work_button = True
    else:
        buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks += 1
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons), all_go_work_button


def isHome(hero, buttons):
    y = hero[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True


def isWorking(bar, buttons):
    y = bar[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True


def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 140

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    logger('🆗 %d buttons detected' % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    hero_clicks_cnt = 0
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks += 1
        hero_clicks_cnt += 1
        if hero_clicks_cnt > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def clickFullBarButtons():
    offset = 100
    full_bars = positions(images['full-stamina'], threshold=ct['default'])
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks += 1

    return len(not_working_full_bars)


def goToHeroes():
    global login_attempts
    if clickBtn(images['go-back-arrow']):
        login_attempts = 0

    # TODO tirar o sleep quando colocar o pulling
    # time.sleep(1)
    if clickBtn(images['hero-icon']):
        time.sleep(randint(1, 3))


def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])


def refreshHeroesPositions():
    logger('🔃 Refreshing Heroes Positions')
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])

    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])


def login():
    global login_attempts
    logger('😿 Checking if game has disconnected')

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl', 'f5')
        return

    if clickBtn(images['connect-wallet'], timeout=10) or clickBtn(images['wallet'], timeout=10):
        logger('🎉 Connect wallet button detected, logging in!')
        login_attempts += 1
        # TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(images['select-wallet-2'], timeout=8) or clickBtn(images['confirm'], timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts += 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        if clickBtn(images['treasure-hunt-icon'], timeout=15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        return
        # click ok button

    if not clickBtn(images['select-wallet-1-no-hover'], ):
        if clickBtn(images['select-wallet-1-hover'], threshold=ct['select_wallet_buttons']):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(images['select-wallet-2'], timeout=20):
        login_attempts += 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(images['treasure-hunt-icon'], timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(images['ok'], timeout=5):
        pass
        print('ok button clicked')


def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len(hero_positions) == 0:
            # TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position, go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if not isWorking(position, go_work_buttons):
                print('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0] + go_home_buttons[0][2] / 2, position[1] + position[3] / 2,
                                     1)
                pyautogui.click()
            else:
                print('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')


def refreshHeroes():
    logger('🏢 Search for heroes to work')
    if clickBtn(images['ok'], timeout=5):
        print('ok button clicked')
        pyautogui.hotkey('ctrl', 'f5')
        time.sleep(1)

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        logger('⚒️ Sending all heroes to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    is_all_go_work = None
    while empty_scrolls_attempts > 0:
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked, is_all_go_work = clickButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts -= 1

        if not is_all_go_work:
            scroll()
            time.sleep(2)

    logger('💪 {} heroes sent to work'.format(hero_clicks))
    goToGame()


def manager(current_window):
    time.sleep(2)
    now = time.time()

    print(f"\nNOW: {now}")
    print(f'\nNOW - CURRENT_WINDOW: {now - current_window["check_for_captcha"]}')
    print(f"\nADD_RANDOM_NESS: {addRandomness(time_out['check_for_captcha'] * 60)}\n")

    if now - current_window["check_for_captcha"] > addRandomness(time_out['check_for_captcha'] * 60):
        current_window["check_for_captcha"] = now
    if now - current_window["heroes"] > addRandomness(time_out['send_heroes_for_work'] * 60):
        current_window["heroes"] = now
        refreshHeroes()
    if now - current_window["login"] > addRandomness(time_out['check_for_login'] * 60):
        sys.stdout.flush()
        current_window["login"] = now
        login()
    if now - current_window["new_map"] > time_out['check_for_new_map_button']:
        current_window["new_map"] = now
        if clickBtn(images['new-map']):
            loggerMapClicked()
    if now - current_window["refresh_heroes"] > addRandomness(time_out['refresh_heroes_positions'] * 60):
        current_window["refresh_heroes"] = now
        refreshHeroesPositions()
    # clickBtn(teasureHunt)
    logger(None, progress_indicator=True)
    sys.stdout.flush()
    time.sleep(1)


def click_next_tab(current_tab):
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab', presses=current_tab, interval=.2)
    time.sleep(.2)
    pyautogui.keyUp('alt')


def main():
    """Main execution setup and loop"""
    global hero_clicks
    global login_attempts
    global last_log_is_progress
    global images

    hero_clicks = 0
    login_attempts = 0
    last_log_is_progress = False

    if ch['enable']:
        global home_heroes
        home_heroes = loadHeroesToSendHome()
    else:
        print('>>---> Home feature not enabled')
    print('\n')

    print(cat)
    time.sleep(7)

    total_tabs = multiple_tabs["total_tabs"]
    for i in range(total_tabs):
        webbrowser.open_new("https://app.bombcrypto.io/webgl/index.html")
        print(f"Abrindo aba {i} ...")
        time.sleep(2)

    if multiple_tabs["control_window"] == "autoclicable":

        last = {number + 1: {
            key: 0 for key in ["login", "heroes", "new_map", "check_for_captcha", "refresh_heroes"]
        } for number in range(total_tabs)}

        current_tab = total_tabs + 1
        last_change_tab = 0

        while True:
            time.sleep(1)
            current_title = run_command(["xdotool getactivewindow getwindowname"])[0].replace("\n", "")
            print(f"\n{current_title}")
            now = time.time()
            if now - last_change_tab > addRandomness(time_out['change_tab'] * 60):
                current_tab -= 1
                if current_tab == 0:
                    current_tab = total_tabs
                    print(f"TOTAL DE ABAS ATINGIDO, REINICIANDO CONTAGEM DE ABAS")
                print(f"\n{json.dumps(last[current_tab], indent=4)}")
                print(f"\nEFETUANDO {current_tab} CLICKS EM TAB...")
                last_change_tab = now
                click_next_tab(current_tab)
                current_title = run_command(["xdotool getactivewindow getwindowname"])[0].replace("\n", "")
                print(current_title)
            if current_title != "bombcrypto - Google Chrome":
                last_change_tab = now
                click_next_tab(current_tab)
            else:
                if now - last[current_tab]["check_for_captcha"] > addRandomness(time_out['check_for_captcha'] * 60):
                    last[current_tab]["check_for_captcha"] = now
                if now - last[current_tab]["heroes"] > addRandomness(time_out['send_heroes_for_work'] * 60):
                    last[current_tab]["heroes"] = now
                    refreshHeroes()
                if now - last[current_tab]["login"] > addRandomness(time_out['check_for_login'] * 60):
                    sys.stdout.flush()
                    last[current_tab]["login"] = now
                    login()
                if now - last[current_tab]["new_map"] > time_out['check_for_new_map_button']:
                    last[current_tab]["new_map"] = now
                    if clickBtn(images['new-map']):
                        loggerMapClicked()
                if now - last[current_tab]["refresh_heroes"] > addRandomness(time_out['refresh_heroes_positions'] * 60):
                    last[current_tab]["refresh_heroes"] = now
                    refreshHeroesPositions()
                # clickBtn(teasureHunt)
                logger(None, progress_indicator=True)
                sys.stdout.flush()
                time.sleep(1)
    else:
        windows = []
        if get_platform() == 'Linux':
            time.sleep(1)
            #  Aqui ele percorre as janelas que estiver escrito bombcrypto
            for window in get_windows_with_title('bombcrypto'):
                if window["title"] == "bombcrypto" and window["application"].count('Google Chrome') >= 1:
                    windows.append({
                        "window": window,
                        "login": 0,
                        "heroes": 0,
                        "new_map": 0,
                        "check_for_captcha": 0,
                        "refresh_heroes": 0
                    })
            # https://askubuntu.com/questions/703628/how-to-close-minimize-and-maximize-a-specified-window-from-terminal
            if len(windows) >= 1:
                print('>>---> %d windows with the name bombcrypto were found' % len(windows))
                while True:
                    for index, current_window in enumerate(windows):
                        # run_command(["xdotool", "search", "--name", f"{current_window['window']['title']}",
                        # "windowraise"])
                        print("IS_MINIMIZED: ", current_window["window"]["is_minimized"])
                        if current_window["window"]["is_minimized"]:
                            run_command(["wmctrl", "-ir", f"{current_window['window']['id']}", "-b",
                                         "add,maximized_vert,maximized_horz"])
                        time.sleep(2)
                        try:
                            run_command(["wmctrl", "-ia", f"{current_window['window']['id']}"])
                        except:
                            print(f"Window {current_window['window']['title']}-{index} is closed!!!")
                            windows.remove(current_window)
                        time.sleep(5)
                        # run_command(["wmctrl", "-ir", f"{current_window['window']['id']}", "-b",
                        # "remove,maximized_vert,maximized_horz"])
                        print('>>---> Current window: %s-%s' % (current_window['window']['title'], index))
                        manager(current_window)
            else:
                print('>>---> No window with the name bombcrypto was found')
        elif get_platform() == 'Windows':
            time.sleep(1)
            #  Aqui ele percorre as janelas que estiver escrito bombcrypto
            for window in pygetwindow.getWindowsWithTitle('bombcrypto'):
                if window.title.count('bombcrypto-bot') >= 1:
                    continue
                windows.append({
                    "window": window,
                    "login": 0,
                    "heroes": 0,
                    "new_map": 0,
                    "check_for_captcha": 0,
                    "refresh_heroes": 0
                })
            if len(windows) >= 1:
                print('>>---> %d windows with the name bombcrypto were found' % len(windows))
                while True:
                    for currentWindow in windows:
                        currentWindow["window"].activate()
                        if not currentWindow["window"].isMaximized:
                            currentWindow["window"].maximize()
                        print('>>---> Current window: %s' % currentWindow["window"].title)
                        time.sleep(2)
                        manager(currentWindow)
            else:
                print('>>---> No window with the name bombcrypto was found')
        else:
            print('>>---> Plataforma não suportada!!!')


if __name__ == '__main__':
    args = sys.argv
    images = load_images()
    time_out = c['time_intervals']
    if len(args) > 1:
        if args[1] == "--chromedriver" or args[1] == '-c':
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.common.exceptions import TimeoutException
            from selenium.webdriver.support.ui import WebDriverWait

            chrome_service = Service('./chromedriver/chromedriver')
            run_chrome()
    else:
        main()
