import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab

from config import FILE_PATH

TEMPLATE_PATH = './templates/'

TEMPLATE_CHOICE_BATTLE = 'template_choice_battle.png'
TEMPLATE_STADIUM = 'template_stadium.png'
TEMPLATE_ENTER_THE_BATTLE = 'template_enter_the_battle.png'
TEMPLATE_BOARD = 'template_board.png'
TEMPLATE_FLAG = 'template_flag.png'
TEMPLATE_CANCEL = 'template_cancel.png'
TEMPLATE_START_STADIUM = 'template_start_stadium.png'
TEMPLATE_ACTIVE_BELL = 'template_active_bell.png'
TEMPLATE_BELL = 'template_bell.png'
TEMPLATE_START_STADIUM_OR_CANCEL = 'template_start_stadium_or_cancel.png'
TEMPLATE_TRAINING = 'template_training.png'
TEMPLATE_CHOICE_PLACE_STADIUM = 'template_choice_place_stadium.png'
TEMPLATE_IN_STADIUM = 'template_in_stadium.png'
TEMPLATE_EXIT_STADIUM = 'template_exit_stadium.png'

PLACE_AROUND_BOARD = 'around_board'
AROUND_BOARD = 'around_board'
TEMPLATE = 'template'
PLACE = 'place'
ALL_PLACE = [
    {
        TEMPLATE: TEMPLATE_BOARD,
        PLACE: PLACE_AROUND_BOARD
    },
    {
        TEMPLATE: TEMPLATE_FLAG,
        PLACE: PLACE_AROUND_BOARD
    },
]

STATE_AROUND_BOARD = 'state_around_board'
STATE_IN_THE_ARENA = 'state_in_the_arena'

COMPLETED = {
    TEMPLATE_BOARD: False,
    TEMPLATE_CANCEL: False,
    TEMPLATE_STADIUM: False,
    TEMPLATE_TRAINING: False,
    TEMPLATE_START_STADIUM: False,
    TEMPLATE_CHOICE_BATTLE: False,
    TEMPLATE_ENTER_THE_BATTLE: False,
    TEMPLATE_START_STADIUM_OR_CANCEL: False,
}


class Bot:
    def __init__(self, commands):
        self.commands = commands
        self.current_screen = self.get_current_screen()
        self.STATE = STATE_AROUND_BOARD
        self.second = 0

    def run(self):
        self.current_screen = self.get_current_screen()

        if self.STATE == STATE_AROUND_BOARD:
            self.state_around_board()
        if self.STATE == STATE_IN_THE_ARENA:
            self.state_in_the_arena()

    def get_place(self):
        self.current_screen = self.get_current_screen()
        # place = self.where_is_it()
        # if place == PLACE_AROUND_BOARD:
        #     self.place_around_board()

    def get_current_screen(self):
        width, height = pyautogui.size()
        base_screen = ImageGrab.grab(bbox=(0, 0, width, height))
        base_screen.save(FILE_PATH + 'bot/base_screen.png')
        img_rgb = cv2.imread('base_screen.png')
        return cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    def get_template(self, template):
        path = TEMPLATE_PATH + template
        img_rgb = cv2.imread(path, 0)
        return img_rgb

    def get_coordinates(self, template):
        width, height = template.shape[::-1]
        search_result = cv2.matchTemplate(self.current_screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(search_result)
        x, y = max_loc
        return ((x + width) + x) / 2, ((y + height) + y) / 2

    def where_is_it(self):
        for place in ALL_PLACE:
            if self.do_you_see_this(self.get_template(place[TEMPLATE])):
                return place[PLACE]

    def do_you_see_this(self, template):
        search_result = cv2.matchTemplate(self.current_screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(search_result >= 0.6)

        # print(loc)

        if len(loc[0]) != 0:
            return True
        else: return False

    def you_do_it(self, template):
        COMPLETED[template] = True

    def turn_back(self, template):
        COMPLETED[template] = False

    def do_you_completed_this(self, template):
        return COMPLETED[template]

    def state_in_the_arena(self):
        if self.do_you_see_this(self.get_template(TEMPLATE_EXIT_STADIUM)):
            print('Вижу выход из арены')
            x, y = self.get_coordinates(self.get_template(TEMPLATE_EXIT_STADIUM))
            self.commands.mouse_move(x, y)
            self.commands.mouse_click()
            print('Арена завершена')
            self.default_settings()

    def default_settings(self):
        self.STATE = STATE_AROUND_BOARD
        self.second = 0
        self.turn_back(TEMPLATE_BOARD)
        self.turn_back(TEMPLATE_CANCEL)
        self.turn_back(TEMPLATE_STADIUM)
        self.turn_back(TEMPLATE_START_STADIUM)
        self.turn_back(TEMPLATE_TRAINING)
        self.turn_back(TEMPLATE_CHOICE_BATTLE)
        self.turn_back(TEMPLATE_ENTER_THE_BATTLE)
        self.turn_back(TEMPLATE_START_STADIUM_OR_CANCEL)

    def state_around_board(self):
        if self.do_you_completed_this(TEMPLATE_BOARD) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_BOARD)):
                print('Пытаюсь найти доску')
                self.you_do_it(TEMPLATE_BOARD)
                x, y = self.get_coordinates(self.get_template(TEMPLATE_BOARD))
                self.commands.mouse_move(x, y)
                self.commands.mouse_right_click()
                return True

        if self.do_you_completed_this(TEMPLATE_CHOICE_BATTLE) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_CHOICE_BATTLE)):
                print('Нашел доску')
                self.you_do_it(TEMPLATE_CHOICE_BATTLE)
                return True
            else:
                self.turn_back(TEMPLATE_BOARD)

        if self.do_you_completed_this(TEMPLATE_STADIUM) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_STADIUM)):
                print('Увидел выбор битвы')
                self.you_do_it(TEMPLATE_STADIUM)
                x, y = self.get_coordinates(self.get_template(TEMPLATE_STADIUM))
                self.commands.mouse_move(x, y)
                self.commands.mouse_click()
                return True
            else:
                self.turn_back(TEMPLATE_CHOICE_BATTLE)

        if self.do_you_completed_this(TEMPLATE_ENTER_THE_BATTLE) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_ENTER_THE_BATTLE)):
                print('Увидел вход')
                self.you_do_it(TEMPLATE_ENTER_THE_BATTLE)
                x, y = self.get_coordinates(self.get_template(TEMPLATE_ENTER_THE_BATTLE))
                self.commands.mouse_move(x, y)
                self.commands.mouse_click()
                return True
            else:
                self.turn_back(TEMPLATE_STADIUM)

        if self.do_you_completed_this(TEMPLATE_CANCEL) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_CANCEL)):
                print('Увидел cancel')
                self.you_do_it(TEMPLATE_CANCEL)
                return True
            else:
                self.turn_back(TEMPLATE_ENTER_THE_BATTLE)

        if self.do_you_completed_this(TEMPLATE_START_STADIUM_OR_CANCEL) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_START_STADIUM_OR_CANCEL)):
                print('Увидел вступление на ристалище')
                self.you_do_it(TEMPLATE_START_STADIUM_OR_CANCEL)
                return True
            else:
                return False

        if self.do_you_completed_this(TEMPLATE_START_STADIUM) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_START_STADIUM)):
                print('Пытаюсь принять предложение')
                self.you_do_it(TEMPLATE_START_STADIUM)
                x, y = self.get_coordinates(self.get_template(TEMPLATE_START_STADIUM))
                self.commands.mouse_move(x, y)
                self.commands.mouse_click()
                return True

        if self.do_you_completed_this(TEMPLATE_TRAINING) != True:
            if self.do_you_see_this(self.get_template(TEMPLATE_TRAINING)):
                print('Я принял предложение')
                self.you_do_it(TEMPLATE_TRAINING)
                return True

        if self.do_you_completed_this(TEMPLATE_TRAINING) == True and self.do_you_completed_this(TEMPLATE_CHOICE_BATTLE) == True and self.do_you_completed_this(TEMPLATE_BOARD) == True:
            if self.do_you_see_this(self.get_template(TEMPLATE_CHOICE_BATTLE)) == False and self.do_you_see_this(self.get_template(TEMPLATE_BOARD)) == False and self.do_you_see_this(self.get_template(TEMPLATE_FLAG)) == False:
                print('Вошел на арену')
                self.STATE = STATE_IN_THE_ARENA
                return True
            else:
                self.second += 1

            if self.second > 20:
                print('Не удалось зайти на арену')
                self.turn_back(TEMPLATE_START_STADIUM_OR_CANCEL)
                self.turn_back(TEMPLATE_START_STADIUM)
                self.turn_back(TEMPLATE_TRAINING)
                self.turn_back(TEMPLATE_CANCEL)
                self.turn_back(TEMPLATE_ENTER_THE_BATTLE)
                return True

    # def place_around_board(self,):
        # if self.do_you_see_this(self.get_template(TEMPLATE_BELL)):
        #     print('yes i do')
        # else: print('no i do not')

