from bot import Bot
import os
import time

try:
    
    user_id = os.environ["ASK_ID"]

except:
    user_id = input("User Id: ")

b = Bot(user_id)

b.driver_init()
b.smart_delete()

# b.toggle_shoutouts()
#b.answer_all()
