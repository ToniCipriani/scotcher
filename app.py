"""Base Flask app"""
import psycopg2
from flask import Flask, g
app = Flask(__name__)

def conn_sql():
    """Connect to DB and returns connection"""
    db_conn = getattr(g, '_db_conn', None)
    if db_conn is None:
        try:
            db_conn = g._db_conn = psycopg2.connect(user="sco_dbo",
                                                    password="Talisker10",
                                                    host="127.0.0.1",
                                                    port="5432",
                                                    database="scotcher")
        except(Exception, psycopg2.Error) as error:
            print("error while connecting to database", error)
    return db_conn

def exec_sql(sql):
    """Execute given SQL statement"""
    db_conn = conn_sql()
    db_cur = db_conn.cursor()
    db_cur.execute(sql)
    record = db_cur.fetchall()
    db_cur.close()
    return record

@app.teardown_appcontext
def discon_sql(exception):
    """Disconnect connection"""
    db_conn = getattr(g, '_db_conn', None)
    if db_conn is not None:
        db_conn.close()

@app.route('/')
def home():
    """Main Page"""
    bottles = exec_sql("SELECT name, distillery, region, age, abv, notes FROM tb_whisky")
    return str(bottles)

if __name__ == "__main__":
    app.run()
