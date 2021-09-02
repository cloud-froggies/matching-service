from typing import Optional,List

from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.param_functions import Query

import  pymysql
import os
import logging 

DB_ENDPOINT = os.environ.get('db_endpoint')
DB_ADMIN_USER = os.environ.get('db_admin_user')
DB_ADMIN_PASSWORD = os.environ.get('db_admin_password')
DB_NAME = os.environ.get('db_name')


app = FastAPI(title='Matching Service',version='0.1')
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)


def get_db_conn():
    try:
        conn = pymysql.connect(host=DB_ENDPOINT, user=DB_ADMIN_USER, passwd=DB_ADMIN_PASSWORD, db=DB_NAME, connect_timeout=5)
        return conn
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        raise



@app.get("/")
def read_root():
    return {"Service": "matching"}


@app.get("/matching")
def read_matching(category:int):
    conn = get_db_conn()
    logger.error(category)
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT id, bid FROM advertiser_campaigns WHERE status = true AND category = %s"
        cursor.execute(query,(category,))

    if (results := cursor.fetchall()):
        return results
    else:
        raise HTTPException(status_code=404, detail= f'No se encontraron campañas para la categoria {category}') 

     


