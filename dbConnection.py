import sqlite3


connection = sqlite3.connect('parking.db')
mycursor = connection.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS users (number_plate text PRIMARY KEY, entered_time text)""")
connection.commit()

connection.commit()
#connection.close()