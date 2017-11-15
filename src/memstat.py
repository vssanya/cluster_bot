import re
import subprocess


def get_meminfo(node_id='master'):
    memtotal = 0
    memfree = 0
    swaptotal = 0
    swapfree = 0

    meminfo = {
        'MemTotal' : memtotal,
        'MemFree' : memfree,
        'SwapTotal' : swaptotal,
        'SwapFree' : swapfree
    }

    try:
        if node_id=='master':
            bytes = subprocess.check_output(['cat', '/proc/meminfo'])
        else:
            bytes = subprocess.check_output(['ssh', node_id, 'cat', '/proc/meminfo'])
        memfile = bytes.decode('utf-8', 'strict').split('\n')

        for k, v in meminfo.items():
            for line in memfile:
                if line.startswith(k):
                    meminfo[k] = int(re.match(r'{0}:\s*(\d*)'.format(k), line).group(1))
    except:
        pass
    return meminfo


def get_nodes_overusing_swap(node_list, overuse_threshold=0.05):
    bad_nodes = []
    swap_total = []
    swap_free = []
    for node in node_list:
        meminfo = get_meminfo(node)
        if meminfo['SwapTotal'] > 0:
            swap_use_share = (meminfo['SwapTotal'] - meminfo['SwapFree']) / meminfo['SwapTotal']
            if swap_use_share > overuse_threshold:
                bad_nodes.append(node)
                swap_total.append(meminfo['SwapTotal'])
                swap_free.append(meminfo['SwapFree'])
    return bad_nodes, swap_total, swap_free


def format_memdata(node_list):
    result = 'Memory usage:'
    for node in node_list:
        result += '\n' + node + ':\t'
        meminfo = get_meminfo(node)
        if meminfo['MemTotal'] > 0:
            result += '  RAM: used {0:.1f}G of {1:.1f}G'.format(
                (meminfo['MemTotal'] - meminfo['MemFree']) / 1048576,
                meminfo['MemTotal'] / 1048576)
        if meminfo['SwapTotal'] > 0:
            result += '  Swap: used {0:.1f}G of {1:.1f}G'.format(
                (meminfo['SwapTotal'] - meminfo['SwapFree']) / 1048576,
                meminfo['SwapTotal'] / 1048576)
        result += '\n'
    return result

