import subprocess
import re


def get_job_name_by_id(job_id):
    res = subprocess.run(['scontrol', 'show', 'JobId={}'.format(job_id)], stdout=subprocess.PIPE)
    search = re.search(r"JobName=(?P<name>\w+)[ \n]", res.stdout.decode())
    if search is None:
        return None
    else:
        return search.group('name')
