"""Base Flask app"""
import psycopg2
from flask import Flask, g
app = Flask(__name__)

if __name__ == "__main__":
    app.run()
