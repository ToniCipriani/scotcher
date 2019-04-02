"""Database connection"""
import psycopg2

try:
    db_conn = psycopg2.connect(user="sco_dbo",
                               password="Talisker10",
                               host="127.0.0.1",
                               port="5432",
                               database="scotcher")
    cursor = db_conn.cursor()
    cursor.execute("SELECT name, distillery, region, age, abv, notes FROM tb_whisky;")
    record = cursor.fetchone()

except(Exception, psycopg2.Error) as error:
    print("error while connecting to database", error)
finally:
    if db_conn:
        cursor.close()
        db_conn.close()
