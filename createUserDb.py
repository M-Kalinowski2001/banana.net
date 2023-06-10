import mysql.connector
import hashlib


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}


conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')


conn.commit()
cursor.close()
conn.close()

print('Table "user_data" created successfully.')