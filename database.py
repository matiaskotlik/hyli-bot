from horny import Horny
import os

from peewee import *
from playhouse.db_url import connect

import config

db = connect(config.DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = db

class HornyCounter(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    count = IntegerField(default=0)

class Quote(BaseModel):
    message_id = BigIntegerField()
    channel_id = BigIntegerField()
    guild_id = BigIntegerField()


db.create_tables([Quote, HornyCounter])

atomic = db.atomic