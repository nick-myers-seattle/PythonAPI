from email.mime.application import MIMEApplication
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr
from typing import Optional
import os

from flask import Flask, session, request
from markupsafe import escape
from flask_cors import CORS, cross_origin
import psycopg2

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("Connection successful")
    except Exception as e:
        print("Error:  " + str(e))
    return conn

connection = create_conn()


def create_tables(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("""
            DROP TABLE IF EXISTS wheelchairs;

            CREATE TABLE IF NOT EXISTS wheelchairs (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                stock INTEGER
            );

            INSERT INTO wheelchairs(name, stock)
            VALUES
            ('manual', 78),
            ('power', 27),
            ('transport', 46),
            ('reclining', 17);
        """)
        print("Wheelchairs table created successfully")

        cursor.execute("""
            DROP TABLE IF EXISTS walkers;

            CREATE TABLE IF NOT EXISTS walkers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                stock INTEGER
            );

            INSERT INTO walkers(name, stock)
            VALUES
            ('standard', 104),
            ('rollator', 15),
            ('folding', 62),
            ('knee', 48);
        """)
        print("Walkers table created successfully")

        cursor.execute("""
            DROP TABLE IF EXISTS canes;

            CREATE TABLE IF NOT EXISTS canes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                stock INTEGER
            );

            INSERT INTO canes(name, stock)
            VALUES
            ('standard', 205),
            ('offset', 139),
            ('multiple-legged', 72),
            ('chair', 23);
        """)
        print("Canes table created successfully")

        cursor.execute("""
            DROP TABLE IF EXISTS crutches;

            CREATE TABLE IF NOT EXISTS crutches (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                stock INTEGER
            );

            INSERT INTO crutches(name, stock)
            VALUES
            ('axillary', 205),
            ('elbow', 139),
            ('gutter', 72),
            ('forearm', 23);
        """)
        print("Crutches table created successfully")

        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error:  " + str(e))


create_tables(connection)


app = Flask(__name__)
CORS(app, origins='http://localhost:4201', methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers='*')

@app.route('/')
def root():
    return {'status': 'ok'}

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/v1/medical-supplies')
def get_medical_supplies():
    return {
        'medical-supplies': ['wheelchairs', 'walkers', 'canes', 'crutches']
    }

@app.route('/v1/wheelchairs')
@cross_origin()
def get_wheelchairs():
    global connection

    try:
        if connection.closed:
            connection = create_conn()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM wheelchairs;")
        wheelchairs = cursor.fetchall()

        connection.commit()
        cursor.close()

        message = {}
        for results in wheelchairs:
            message[results[1]] = results[2]

        print(message)

        return message
    except Exception as e:
        print("Error:  " + str(e))
        return {}

@app.route('/v1/walkers')
def get_walkers():
    global connection

    try:
        if connection.closed:
            connection = create_conn()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM walkers;")
        wheelchairs = cursor.fetchall()

        connection.commit()
        cursor.close()

        message = {}
        for results in wheelchairs:
            message[results[1]] = results[2]

        print(message)

        return message
    except Exception as e:
        print("Error:  " + str(e))
        return {}

@app.route('/v1/canes')
def get_canes():
    global connection

    try:
        if connection.closed:
            connection = create_conn()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM canes;")
        wheelchairs = cursor.fetchall()

        connection.commit()
        cursor.close()

        message = {}
        for results in wheelchairs:
            message[results[1]] = results[2]

        print(message)

        return message
    except Exception as e:
        print("Error:  " + str(e))
        return {}

@app.route('/v1/crutches')
def get_crutches():
    global connection

    try:
        if connection.closed:
            connection = create_conn()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crutches;")
        wheelchairs = cursor.fetchall()

        connection.commit()
        cursor.close()

        message = {}
        for results in wheelchairs:
            message[results[1]] = results[2]

        print(message)

        return message
    except Exception as e:
        print("Error:  " + str(e))
        return {}

@app.route('/v1/send-email', methods=['POST'])
def send_email():
    try:
        password = os.getenv('EMAIL_ADDRESS_AUTOMATED_PASSWORD')
        from_address = os.getenv("EMAIL_ADDRESS_AUTOMATED")
        to_address = sanitize_email_address(request.json.get('email'))
        if to_address is None:
            raise Exception("Invalid email address")

        message = MIMEMultipart()
        message['From'] = from_address
        message['To'] = to_address
        message['CC'] = os.getenv("EMAIL_ADDRESS_PERSONAL")
        message['Subject'] = 'Nick\'s Python API Server Email'
        body = 'Thank you for using my app!  My resume is attached.'
        message.attach(MIMEText(body, 'plain'))

        try:
            with open('NickMyersResume.pdf', 'rb') as file:
                resume = MIMEApplication(file.read(), Name='NickMyersResume.pdf')
                resume['Content-Disposition'] = 'attachment; filename="NickMyersResume.pdf"'
                message.attach(resume)
        except Exception as e:
            print("Error:  " + str(e))

        email_server = smtplib.SMTP('smtp.gmail.com: 587')
        email_server.ehlo()
        email_server.starttls()
        email_server.login(from_address, password)
        email_server.sendmail(from_address, [to_address, os.getenv("EMAIL_ADDRESS_PERSONAL")], message.as_string())
        email_server.quit()

        return {
            'status': 'ok'
        }

    except Exception as e:
        print("Error:  " + str(e))
        return {
            'status': 'error'
        }
    
def sanitize_email_address(email_address: str) -> Optional[str]:
    email_address = escape(email_address) # sanitize input

    if not email_address:
        return None
    
    # Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email_address):
        return None

    return email_address

if __name__ == '__main__':
    app.run()
