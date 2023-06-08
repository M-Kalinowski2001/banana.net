import mysql.connector
import hashlib

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}

users = [
    {
        'username': 'user1',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone_number': '1234567890',
        'password': 'password1'
    },
    {
        'username': 'user2',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'janesmith@example.com',
        'phone_number': '9876543210',
        'password': 'password2'
    },
    {
        'username': 'user3',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alicejohnson@example.com',
        'phone_number': '5555555555',
        'password': 'password3'
    }

]

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

for user in users:
    hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()

    sql = '''
        INSERT INTO user_data (username, first_name, last_name, email, phone_number, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (
        user['username'],
        user['first_name'],
        user['last_name'],
        user['email'],
        user['phone_number'],
        hashed_password
    )

    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()

print('User data added to the database.')
