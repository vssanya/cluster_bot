import os

token = os.environ.get('TB_TOKEN')

host = os.environ.get('CB_HOST', 'localhost')
port = os.environ.get('CB_PORT', 8080)

update_time = 60*10
crit_temp = 30
