import os

from peewee import *
from playhouse.db_url import connect

import config

db = connect(config.DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = db


class Quote(BaseModel):
    message_id = BigIntegerField()
    channel_id = BigIntegerField()
    guild_id = BigIntegerField()


db.create_tables([Quote])
