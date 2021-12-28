import psycopg2
import bcrypt
import logging


class Postgres:
  # Setting up loggers filename, append mode and format
  logging.basicConfig(filename="logfile.log",
                      filemode='a',
                      format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

  # Constants used to connect to a database 
  DB_HOST = "localhost"
  DB_NAME = "librarydb"
  DB_USER = "postgres"
  DB_PASS = "postgres"

  # Function to compare passwords
  def comparePassword(self, mail, password):
    conn = psycopg2.connect(dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS, host=self.DB_HOST)
    c = conn.cursor()

    # Pulling the hashed password from the database
    try:
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

      # Using bcrypt to compare the password to the one we typed
      if bcrypt.checkpw(password.encode(), result.encode()) == True:
        return True
      elif bcrypt.checkpw(password.encode(), result.encode()) == False:
        logging.warning('Wrong password entered with ' + mail + ' mail')
        return False 
    except IndexError:
      conn.rollback() # Transaction rollback if something goes wrong
      logging.warning('IndexError: Non-Existent Mail')
      return "Non-Existent Mail"

    c.close()
    conn.close()
    
