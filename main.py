from bot import Bot
import os
import time

user_id = os.environ["ASK_ID"]


b = Bot(user_id)

b.driver_init()
# b.toggle_shoutouts()
b.answer_all()
