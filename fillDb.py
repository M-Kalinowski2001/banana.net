import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}

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
        'name': 'Anise',
        'price': 42.39,
        'quantity': 15,
        'country_of_origin': 'North Africa'
    },
    {
        'name': 'Bay leaf',
        'price': 4.49,
        'quantity': 15,
        'country_of_origin': 'Greece'
    },
    {
        'name': 'Cardamom',
        'price': 2.49,
        'quantity': 102,
        'country_of_origin': 'South Asia'
    },
    {
        'name': 'Catnip',
        'price': 14.89,
        'quantity': 30,
        'country_of_origin': 'Eurasia'
    },
    {
        'name': 'Cayenne Pepper',
        'price': 34.89,
        'quantity': 300,
        'country_of_origin': 'French Guiana'
    },
    {
        'name': 'Chives',
        'price': 6.29,
        'quantity': 28,
        'country_of_origin': 'Europe'
    },
    {
        'name': 'Curry',
        'price': 15.49,
        'quantity': 400,
        'country_of_origin': 'India'
    },
    {
        'name': 'Ginger',
        'price': 14.89,
        'quantity': 30,
        'country_of_origin': 'Asia'
    },
    {
        'name': 'Lavender',
        'price': 24.00,
        'quantity': 25,
        'country_of_origin': 'Europe'
    },
    {
        'name': 'Licorice',
        'price': 50.00,
        'quantity': 153,
        'country_of_origin': 'Southern Europe'
    },
    {
        'name': 'Oregano',
        'price': 2.79,
        'quantity': 400,
        'country_of_origin': 'Italy'
    },
    {
        'name': 'Rosemary',
        'price': 14.99,
        'quantity': 10,
        'country_of_origin': 'Europe'
    },
    {
        'name': 'Sesame',
        'price': 4.89,
        'quantity': 300,
        'country_of_origin': 'Africa'
    },
    {
        'name': 'Spearmint',
        'price': 8.99,
        'quantity': 34,
        'country_of_origin': 'North America'
    },
    {
        'name': 'Vanilla',
        'price': 14.89,
        'quantity': 60,
        'country_of_origin': 'Mexico'
    },
    {
        'name': 'Wasabi',
        'price': 100.00,
        'quantity': 5,
        'country_of_origin': 'Japan'
    },
]

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

for product in products:
    sql = '''
        INSERT INTO products (name, price, quantity, country_of_origin)
        VALUES (%s, %s, %s, %s)
    '''
    values = (product['name'], product['price'], product['quantity'], product['country_of_origin'])
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()

print('Product information added to the database.')
