from flask import Flask
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
