# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
import json
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def get_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify({
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }), 200
    else:
        return jsonify({'message': 'Earthquake 9999 not found.'}), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_mag(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quake_list = [
        {
            'id': quake.id,
            'magnitude': quake.magnitude,
            'location': quake.location,
            'year': quake.year
        }
        for quake in earthquakes
    ]
    
    response = {
        'count': len(quake_list),
        'quakes': quake_list
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
