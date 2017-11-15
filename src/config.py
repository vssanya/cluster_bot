import os

token = os.environ.get('TB_TOKEN')

host = os.environ.get('CB_HOST', 'localhost')
port = os.environ.get('CB_PORT', 8080)

temp_update_time = 60*10
crit_temp = 30

swap_update_time_multiplier = 3 # checking swap usage X times less often than temp
swap_overuse_threshold = 0.05

node_list = ['master',
    'n01', 'n02', 'n03', 'n04', 'n05', 'n06', 'n07', 'n08', 'n09', 'n10',
    'n11', 'n12', 'n13', 'n14', 'n15', 'n16', 'n17', 'n18', 'n19', 'n20',
           'n22', 'n23', 'n24', 'n25', 'n26', 'n27', 'n28', 'n29', 'n30',
    'n31', 'n32', 'n33', 'n34', 'n35', 'n36', 'n37', 'n38']

