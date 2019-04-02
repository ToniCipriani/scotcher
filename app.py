"""Base Flask App"""
import psycopg2
from flask import Flask, g

CONN_STRING = user="sco_dbo",password="Talisker10",host="localhost",port="5432",database="scotcher"

app = Flask(__name__)

def conn_sql():
"""Connect to DB and returns connection"""
    db_conn = getattr(g,'_db_conn',None)
	if db_conn == None:
	    try:
		    db_conn = g._db_conn = psycopg2.connect(CONN_STRING)
        except(Exception, psycopg2.Error) as error:
            print("error while connecting to database", error)
	return db_conn:

def exec_sql(sql):
"""Execute given SQL statement"""
	db_conn = conn_sql()
	db_cur = db_conn.cursor()
	db_cur.execute(sql)
    record = db_cur.fetchall()
	db_cur.close()
	return record

def discon_sql():
"""Disconnect connection"""
	db_conn = getattr(g,'_db_conn',None)
    if db_conn:
        db_conn.close()

@app.route('/')
def home():
	bottles = exec_sql(SELECT name, distillery, region, age, abc, notes FROM tb_whisky)
	return bottles
	