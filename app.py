from flask import Flask, session
from flask_cors import CORS, cross_origin
import psycopg2
import os

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host ="pythonapiserver-server.postgres.database.azure.com",
            database="pythonapiserver-database",
            user="rjgjoogces",
            password=os.getenv("AZUREDBPASSWORD")
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

if __name__ == '__main__':
    app.run()
