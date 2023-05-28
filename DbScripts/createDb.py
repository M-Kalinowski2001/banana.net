import mysql.connector

# Connect to the MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

# Create a new database
cursor = conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS spice_store')
cursor.execute('USE spice_store')

# Create a table for products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        quantity INT NOT NULL,
        country_of_origin VARCHAR(255) NOT NULL
    )
''')

# Close the connection to the MySQL server
cursor.close()
conn.close()

# Create a file for connecting to the database using Flask
with open('db.py', 'w') as file:
    file.write('''\
import mysql.connector
from flask import Flask

app = Flask(__name__)

def get_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='spice_store'
    )
    return conn

@app.teardown_appcontext
def close_db(error):
    if hasattr(Flask, 'db'):
        Flask.db.close()

if __name__ == '__main__':
    app.run(debug=True)
''')

print("MySQL database and Flask connection file created successfully.")