from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import hashlib

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spice_store'
}


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
