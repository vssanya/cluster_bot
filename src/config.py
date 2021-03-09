import os

token = os.environ.get('TB_TOKEN')

host = os.environ.get('CB_HOST', '10.10.0.254')
port = os.environ.get('CB_PORT', 8080)

temp_update_time = 60*2
mem_update_time = 60*60*2

crit_temp = 29

swap_overuse_threshold = 0.05

node_list = [
    'master',
    'n01', 'n02', 'n03', 'n04', 'n05', 'n06', 'n07', 'n08', 'n09', 'n10',
    'n11', 'n12', 'n13', 'n14', 'n15', 'n16', 'n17', 'n18', 'n19', 'n20',
    'n21', 'n22', 'n23', 'n24', 'n25', 'n26', 'n27', 'n28', 'n29', 'n30',
    'n31', 'n33', 'n33', 'n34', 'n35', 'n36', 'n37', 'n38']

webhook_url_base = 'https://telbotproxy.herokuapp.com'
webhook_url_path = '/bot/{}/'.format(token)

webhook_host = 'localhost'
webhook_port = 8007
