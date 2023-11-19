from flask import Flask
import psycopg2
import os

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            host ="pythonapiserver-server.postgres.database.azure.com",
            database="pythonapiserver-database",
            user="rjgjoogces",
            password="spaceNeedle1!",
        )
        print("Connection successful")
    except Exception as e:
        print("Error:  " + str(e))
    return conn

connection = create_conn()


def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DROP TABLE wheelchairs;

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

            SELECT * FROM wheelchairs;
        """)
        print("Table created successfully")

        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error:  " + str(e))


create_table(connection)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'message': 'hi'}

@app.route('/v1/medical-supplies')
def get_medical_supplies():
    return {
        'medical-supplies': ['wheelchairs', 'walkers', 'canes', 'crutches']
    }

@app.route('/v1/wheelchairs')
def get_wheelchairs():
    return {
        'wheelchairs': ['manual', 'power', 'transport', 'reclining']
    }

@app.route('/v1/walkers')
def get_walkers():
    return {
        'walkers': ['standard', 'rollator', 'folding', 'knee']
    }

@app.route('/v1/canes')
def get_canes():
    return {
        'canes': ['standard', 'offset', 'multiple-legged', 'chair']
    }

@app.route('/v1/crutches')
def get_crutches():
    return {
        'crutches': ['axillary', 'elbow', 'gutter', 'forearm']
    }

if __name__ == '__main__':
    app.run()
