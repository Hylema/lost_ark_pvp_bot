import time
from ahk import AHK

from bot import Bot
from bot_commands import BotCommands

bot = Bot(BotCommands(AHK()))

while True:
    place = bot.run()
    time.sleep(1)

