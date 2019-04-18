import uuid
from django.db import connection

def uuidToStr():
    return str(uuid.uuid4())


def executeSQL(sql):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        return(res)
