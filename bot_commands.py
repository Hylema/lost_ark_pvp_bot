class BotCommands:
    def __init__(self, ahk):
        self.ahk = ahk

    def default_position(self):
        self.ahk.mouse_position = (0, 0)

    def mouse_move(self, x, y):
        self.ahk.mouse_position = (0, 0)
        self.ahk.mouse_move(x, y, speed=10, relative=True)

    def mouse_click(self):
        self.ahk.click()

    def mouse_right_click(self):
        self.ahk.right_click()

    def keyword_press(self, keyword):
        self.ahk.key_press(keyword)

