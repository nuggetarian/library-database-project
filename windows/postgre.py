import psycopg2

class Postgres:

  DB_HOST = "localhost"
  DB_NAME = "hahaha"
  DB_USER = "postgres"
  DB_PASS = "postgres"

  def createTable(self):
    conn = psycopg2.connect(dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST)
    c = conn.cursor()

    c.execute("CREATE TABLE sqlinjectiontable1 (id SERIAL PRIMARY KEY, name VARCHAR)")
    conn.commit()

    c.close()
    conn.close()
