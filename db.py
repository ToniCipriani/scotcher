"""Database connection"""
import psycopg2

try:
    DB_CONN = psycopg2.connect(user="sco_dbo",
                               password="Talisker10",
                               host="localhost",
                               port="5432",
                               database="scotcher")
    CURSOR = DB_CONN.CURSOR()
    CURSOR.execute("SELECT * FROM tb_whisky;")
    RECORD = CURSOR.fetchone()
    print(RECORD)

except(Exception, psycopg2.Error) as error:
    print("error while connecting to database", error)
finally:
    if DB_CONN:
        CURSOR.close()
        DB_CONN.close()
