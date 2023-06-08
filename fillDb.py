import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}

# Sample product information
products = [
    {
        'name': 'Cinnamon',
        'price': 5.99,
        'quantity': 10,
        'country_of_origin': 'Sri Lanka'
    },
    {
        'name': 'Turmeric',
        'price': 4.49,
        'quantity': 15,
        'country_of_origin': 'India'
    },
    {
        'name': 'Paprika',
        'price': 3.99,
        'quantity': 8,
        'country_of_origin': 'Hungary'
    },
{
        'name': 'Pepper',
        'price': 21.37,
        'quantity': 69,
        'country_of_origin': 'Poland'
    },
{
        'name': 'Truffle',
        'price': 699.21,
        'quantity': 37,
        'country_of_origin': 'Africa'
    },
{
        'name': 'Koks',
        'price': 420.37,
        'quantity': 21,
        'country_of_origin': 'Colombia'
    }
    # Add more products here
]

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Insert product information into the table
for product in products:
    sql = '''
        INSERT INTO products (name, price, quantity, country_of_origin)
        VALUES (%s, %s, %s, %s)
    '''
    values = (product['name'], product['price'], product['quantity'], product['country_of_origin'])
    cursor.execute(sql, values)

# Commit the changes and close the database connection
conn.commit()
cursor.close()
conn.close()

print('Product information added to the database.')