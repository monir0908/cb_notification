from mongoengine import connect

from configs import MONGO_URL


def init_db_conn(loop):
    db = connect(host=MONGO_URL)
    return loop, db
