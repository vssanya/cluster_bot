# Input should look like this for an end record:
# $1: '-s' (the subject argument keyword)
# $2: The subject itself
# $3: The To: email address.
#
# The subject should look like this for an start record:
# SLURM Job_id=323 Name=ddt_clone Began, Queued time 00:00:01
#
# The subject should look like this for an end record:
# SLURM Job_id=327 Name=ddt_clone Ended, Run time 00:05:01, COMPLETED, ExitCode 0
# SLURM Job_id=328 Name=ddt_clone Failed, Run time 00:05:01, FAILED, ExitCode 127
# SLURM Job_id=342 Name=ddt_clone Ended, Run time 00:00:33, CANCELLED, ExitCode 0
# Not sure what to do about PENDING state resulting from a requeue request.
# Doing a seff on it for now:
# SLURM Job_id=326 Name=ddt_clone Failed, Run time 00:00:41, PENDING, ExitCode 0
#
# These end records are the only types of messages to process. They have 4 (rather
# than 2) comma-delimited arguments, of which ending status is the 3rd.
# Just pass through notifications without an ending status.

import argparse
import re
import subprocess

import models
import bot


def slurm_get_user(job_id):
    res = subprocess.run(['scontrol', 'show', 'JobId={}'.format(job_id)], stdout=subprocess.PIPE)
    return re.search('UserId=(?P<username>\w+)', res.stdout.decode('utf-8')).groupdict()['username']

parser = argparse.ArgumentParser(description='BotMail programm for slurm')
parser.add_argument('-s', dest='subject', type=str)
parser.add_argument('email', type=str)

args = parser.parse_args()

if args.email == 'telegram':
    info = re.search('Job_id=(?P<id>\d+) Name=(?P<name>\w+).*, (?P<state>[A-Z][A-Z]+),', args.subject).groupdict()
    username = slurm_get_user(info['id'])

    user = models.User.select().where(models.User.username == username).get()
    chat = models.Chat.select().where(models.Chat.user == user).get()

    bot.bot.send_message(chat.id, args.subject)
else:
    pass
