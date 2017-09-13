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


class Job(Model):
    id = IntegerField(unique=True)
    user = ForeignKeyField(User, related_name='jobs')

    start_time = DateTimeField(default=datetime.datetime.now)
    status = FloatField(default=0.0)

    prediction_end_time = DateTimeField(null=True)

    class Meta:
        database = db
