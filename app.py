import secrets

from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector

from fillDb import products
from loginForm import hash_password

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['TEMPLATES_AUTO_RELOAD'] = True

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}


def get_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, price, quantity, country_of_origin FROM products')
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products


def get_product_by_id(product_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, price, quantity, country_of_origin FROM products WHERE id=%s', (product_id,))
    product = cursor.fetchone()

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


@app.route('/', methods=['GET'])
def home():
    search_query = request.args.get('search', '').capitalize()

    if search_query:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM products WHERE name LIKE %s
        ''', (f'%{search_query}%',))

        products = cursor.fetchall()

        cursor.close()
        conn.close()
    else:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM products
        ''')

        products = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('index.html', products=products, search_query=search_query)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM user_data
            WHERE username = %s AND password = %s
        ''', (username, hashed_password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result[0] > 0:

            session['username'] = username

            return redirect(url_for('login_success'))
        else:
            return render_template('login.html', error_message='Invalid username or password')

    return render_template('login.html')


@app.route('/login_success', methods=['GET'])
def login_success():
    search_query = request.args.get('search', '').capitalize()

    if 'username' in session:
        if search_query:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM products WHERE name LIKE %s
            ''', (f'%{search_query}%',))

            products = cursor.fetchall()

            cursor.close()
            conn.close()
        else:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM products
            ''')

            products = cursor.fetchall()

            cursor.close()
            conn.close()

        return render_template('main_site.html', products=products, search_query=search_query)
    else:
        return redirect(url_for('login'))


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

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username already exists in the database
        cursor.execute('SELECT username FROM user_data WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return render_template('register.html', error_message='Username already exists. Please choose a different '
                                                                  'username.')

        cursor.execute('''
                INSERT INTO user_data (username, first_name, last_name, email, phone_number, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (username, first_name, last_name, email, phone_number, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('login', success_message='Registration successful. You can now login.'))

    return render_template('register.html')
def get_user_data(username):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, username, first_name, last_name, email, phone_number, password FROM user_data WHERE username = %s',
        (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return user_data


@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' in session:
        username = session['username']

        if request.method == 'POST':
            if 'delete_account' in request.form:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                cursor.execute('DELETE FROM user_data WHERE username = %s', (username,))
                conn.commit()

                cursor.close()
                conn.close()

                session.pop('username', None)
                flash('Your account has been successfully deleted.', 'success')

                return redirect(url_for('home'))

            new_username = request.form['username']
            new_email = request.form['email']
            new_phone_number = request.form['phone_number']
            new_password = request.form['password']

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

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

            cursor.close()
            conn.close()

            flash('Your account information has been successfully updated.', 'success')

            return redirect(url_for('account'))

        user_data = get_user_data(username)
        return render_template('account.html', user_data=user_data)

    else:
        return redirect(url_for('login'))


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM user_data WHERE username = %s', (username,))
        conn.commit()

        cursor.close()
        conn.close()

        session.pop('username', None)
        flash('Your account has been successfully deleted.', 'success')

        return redirect(url_for('home'))

    return redirect(url_for('login'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    product_info = get_product_by_id(product_id)
    name = product_info[0]
    price = float(product_info[1])

    item = {
        'product_id': product_id,
        'name': name,
        'price': price,
        'quantity': quantity,
    }

    cart_items = session.get('cart', [])

    cart_items.append(item)

    session['cart'] = cart_items

    if 'username' in session:
        return redirect('/login_success')
    else:
        return redirect('/')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = session.get('cart', [])

    if request.method == 'POST':

        product_id = request.form['product_id']

        cart_items = session.get('cart', [])

        for item in cart_items:
            if item['product_id'] == product_id:
                cart_items.remove(item)
                break
        session['cart'] = cart_items

    cart_items = session.get('cart', [])

    total_price = 0
    for item in cart_items:
        product_info = get_product_by_id(item['product_id'])
        if product_info[1] is not None:
            total_price += product_info[1] * item['quantity']

    is_logged_in = 'username' in session

    if is_logged_in:
        return render_template('userCart.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('cart.html', cart_items=cart_items, total_price=total_price, is_logged_in=is_logged_in)


def remove_product_from_cart(product_id):
    cart_items = session.get('cart', [])
    updated_cart = [item for item in cart_items if item['product_id'] != product_id]
    session['cart'] = updated_cart


@app.route('/checkout')
def checkout():
    is_logged_in = 'username' in session

    if is_logged_in:
        return render_template('checkoutUser.html')
    else:
        return render_template('checkout.html')


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
