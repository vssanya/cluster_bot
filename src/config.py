import os

token = os.environ.get('TB_TOKEN')
white_chat_list = list(map(int, os.environ.get('TB_WCL').split(':')))

update_time = 60*10
crit_temp = 30
