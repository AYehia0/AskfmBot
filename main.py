import os
from bot import Bot

# Hidden ID
user_id = os.environ['ASK_ID']

b = Bot(user_id)

b.driver_init()
