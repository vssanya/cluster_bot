import uuid
import datetime
from peewee import *


db = SqliteDatabase('bot.db')


class User(Model):
    username = CharField(unique=True)
    token = UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        database = db


class Chat(Model):
    id = IntegerField(unique=True)
    # if null == True it's group
    user = ForeignKeyField(User, related_name='chats', null=True)

    class Meta:
        database = db


class JobStatus(Model):
    job_id = IntegerField()
    user = ForeignKeyField(User, related_name='jobs')

    time = DateTimeField(default=datetime.datetime.now)
    status = FloatField(default=0.0)

    class Meta:
        database = db
