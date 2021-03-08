from bot import Bot
import os 

user_id = os.environ["ASK_ID"]


b = Bot(user_id)

b.driver_init()
b.get_last_question()
b.toggle_shoutouts()