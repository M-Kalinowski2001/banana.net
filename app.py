import secrets

from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector

from fillDb import products
from loginForm import hash_password

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Replace with your secret key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}


def get_products():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch product information from the database
    cursor.execute('SELECT id, name, price, quantity, country_of_origin FROM products')
    products = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return products


def get_product_by_id(product_id):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch product information from the database based on the product ID
    cursor.execute('SELECT id, name, price, quantity, country_of_origin FROM products WHERE id=%s', (product_id,))
    product = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    if product is not None:
        return product[1], float(product[2])

    return None, None


def get_cart_items():
    if 'cart' in session:
        return session['cart']
    else:
        return []


@app.route('/')
def home():
    # Get the product information from the database
    products = get_products()

    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username and hashed password exist in the user_data table
        cursor.execute('''
            SELECT COUNT(*) FROM user_data
            WHERE username = %s AND password = %s
        ''', (username, hashed_password))
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        if result[0] > 0:
            # Set the username in the session
            session['username'] = username

            return redirect(url_for('login_success'))
        else:
            return render_template('login.html', error_message='Invalid username or password')

    return render_template('login.html')


@app.route('/login_success')
def login_success():
    return render_template('main_site.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        hashed_password = hash_password(password)

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert user data into the user_data table
        cursor.execute('''
                INSERT INTO user_data (username, first_name, last_name, email, phone_number, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (username, first_name, last_name, email, phone_number, hashed_password))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        return redirect(url_for('login', success_message='Registration successful. You can now login.'))

    return render_template('register.html')


def get_user_data(username):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch the user data from the user_data table based on the username
    cursor.execute(
        'SELECT id, username, first_name, last_name, email, phone_number, password FROM user_data WHERE username = %s',
        (username,))
    user_data = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    return user_data


@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' in session:
        username = session['username']

        if request.method == 'POST':
            if 'delete_account' in request.form:
                # Connect to the database
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                # Delete the user data from the user_data table based on the username
                cursor.execute('DELETE FROM user_data WHERE username = %s', (username,))
                conn.commit()

                # Close the database connection
                cursor.close()
                conn.close()

                # Clear the session data and display a success message
                session.pop('username', None)
                flash('Your account has been successfully deleted.', 'success')

                # Redirect to the home page (index.html)
                return redirect(url_for('home'))

            new_username = request.form['username']
            new_email = request.form['email']
            new_phone_number = request.form['phone_number']
            new_password = request.form['password']

            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Update user data in the user_data table
            if new_password:
                hashed_password = hash_password(new_password)
                cursor.execute('''
                    UPDATE user_data
                    SET username = %s, email = %s, phone_number = %s, password = %s
                    WHERE username = %s
                ''', (new_username, new_email, new_phone_number, hashed_password, username))
            else:
                cursor.execute('''
                    UPDATE user_data
                    SET username = %s, email = %s, phone_number = %s
                    WHERE username = %s
                ''', (new_username, new_email, new_phone_number, username))

            conn.commit()

            # Close the database connection
            cursor.close()
            conn.close()

            # Display a success message
            flash('Your account information has been successfully updated.', 'success')

            # Redirect to the account page
            return redirect(url_for('account'))

        # Fetch the user data
        user_data = get_user_data(username)
        return render_template('account.html', user_data=user_data)

    else:
        return redirect(url_for('login'))


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Delete the user data from the user_data table based on the username
        cursor.execute('DELETE FROM user_data WHERE username = %s', (username,))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Clear the session data and display a success message
        session.pop('username', None)
        flash('Your account has been successfully deleted.', 'success')

        # Redirect to the home page (index.html)
        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    # Get the product information
    product_info = get_product_by_id(product_id)
    name = product_info[0]
    price = float(product_info[1])

    # Create a new cart item dictionary
    item = {
        'product_id': product_id,
        'name': name,
        'price': price,
        'quantity': quantity,
    }

    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Add the new item to the cart
    cart_items.append(item)

    # Store the updated cart items in the session
    session['cart'] = cart_items

    # Redirect back to the homepage
    return redirect('/')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    if request.method == 'POST':
        # Retrieve the product ID from the form
        product_id = request.form['product_id']

        # Retrieve the cart items from the session
        cart_items = session.get('cart', [])

        # Remove the product from the cart
        for item in cart_items:
            if item['product_id'] == product_id:
                cart_items.remove(item)
                break

        # Update the cart items in the session
        session['cart'] = cart_items

        # Retrieve the cart items from the session
    cart_items = session.get('cart', [])

    # Calculate the total price of the items in the cart
    total_price = 0
    for item in cart_items:
        product_info = get_product_by_id(item['product_id'])
        if product_info[1] is not None:
            total_price += product_info[1] * item['quantity']

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


def remove_product_from_cart(product_id):
    cart_items = session.get('cart', [])
    updated_cart = [item for item in cart_items if item['product_id'] != product_id]
    session['cart'] = updated_cart


@app.route('/checkout')
def checkout():
    if 'username' in session:
        cart_items = get_cart_items()
        cart_total = sum(item['total_price'] for item in cart_items)

        return render_template('checkout.html', cart_items)


@app.route('/change_address')
def change_address():
    if 'username' in session:
        return render_template('change_address.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)
