import secrets

from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
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
    cursor.execute('SELECT name, price, quantity, country_of_origin FROM products')
    products = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return products

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
    cursor.execute('SELECT id, username, first_name, last_name, email, phone_number, password FROM user_data WHERE username = %s', (username,))
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

                # Retrieve the ID of the user based on the current username
                cursor.execute('SELECT id FROM user_data WHERE username = %s', (username,))
                user_id = cursor.fetchone()[0]

                # Delete the user data from the user_data table based on the retrieved ID
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

        # Fetch the updated user data after updating or deleting the account
        user_data = get_user_data(username)
        return render_template('account.html', user_data=user_data)

    else:
        return redirect(url_for('login'))
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