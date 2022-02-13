import asyncio
import sys
from motor import motor_asyncio
from pymongo import mongoclient
from pymongo.errors import serverselectiontimeouterror
from Takanashirika import mongo_db_uri
from Takanashirika.confing import get_int_key, get_str_key


mongo_port = get_int_key("27017")
mongo_db_uri = get_str_key("mongo_db_uri")
mongo_db = "skyzurobot"


client = mongoclient()
client = mongoclient(mongo_db_uri, mongo_port)[mongo_db]
motor = motor_asyncio.asynciomotorclient(mongo_db_uri, mongo_port)
db = motor[mongo_db]
db = client["emiexrobot"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except serverselectiontimeouterror:
    sys.exit(log.critical("can't connect to mongodb! exiting..."))
