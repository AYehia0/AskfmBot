from bot import Bot
import os 

user_id = os.environ["ASK_ID"]


b = Bot(user_id)

b.driver_init()
b.answer_question("Hello Darkness my old friend")