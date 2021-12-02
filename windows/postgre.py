from tkinter import mainloop
import psycopg2
import bcrypt

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
  
  """def addPassword(self):
    password = "batman"
    hashPw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print(hashPw)

    conn = psycopg2.connect(dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST)
    c = conn.cursor()

    for i in range(52):
      c.execute("UPDATE public.user SET password=%s WHERE user_id=%s;",(hashPw.decode(), i+1))
    c.execute("UPDATE public.user SET password=%s WHERE user_id=%s;",(hashPw.decode(), 53))
    conn.commit()


    c.close()
    conn.close()"""

  def comparePassword(self, mail, password):
    conn = psycopg2.connect(dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST)
    c = conn.cursor()

    c.execute("""SELECT
                  u.password
                FROM
                  public.user u
                JOIN
                  public.contact c ON u.user_id = c.user_id
                WHERE c.mail = %s""", (mail,))
    conn.commit()
    find = c.fetchall()
    result = find[0][0]

    if bcrypt.checkpw(password.encode(), result.encode()) == True:
      return True
    elif bcrypt.checkpw(password.encode(), result.encode()) == False:
      return False

    c.close()
    conn.close()
    
