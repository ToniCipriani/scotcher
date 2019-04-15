"""Database connection"""
import psycopg2
from flask import current_app, g

def conn_sql():
    """Connect to DB and returns connection"""
    db_conn = getattr(g, '_db_conn', None)
    if db_conn is None:
        try:
            db_conn = g._db_conn = psycopg2.connect(current_app.config['DATABASE'])
        except(Exception, psycopg2.Error) as error:
            print("error while connecting to database", error)
    return db_conn

def discon_sql(exception):
    """Disconnect connection"""
    db_conn = getattr(g, '_db_conn', None)
    if db_conn is not None:
        db_conn.close()

def init_app(app):
    """DB init app"""
    app.teardown_appcontext(discon_sql)
