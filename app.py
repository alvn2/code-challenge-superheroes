#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

# Set up the database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# API Setup
api = Api(app)

class HeroResource(Resource):
    def get(self, hero_id):
        hero = Hero.query.get_or_404(hero_id)
        return hero.to_dict(serialize_rules=('-hero_powers.power',)), 200

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'super_name' not in data:
            return {'message': 'Bad request: Name and Super Name are required'}, 400
        try:
            new_hero = Hero(**data)
            db.session.add(new_hero)
            db.session.commit()
            return new_hero.to_dict(), 201
        except Exception as e:
            return {'message': str(e)}, 400

class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get_or_404(power_id)
        return power.to_dict(), 200

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Bad request: Name is required'}, 400
        try:
            new_power = Power(**data)
            db.session.add(new_power)
            db.session.commit()
            return new_power.to_dict(), 201
        except Exception as e:
            return {'message': str(e)}, 400

class HeroesListResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict(serialize_rules=('-hero_powers.power',)) for hero in heroes], 200

class PowersListResource(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict() for power in powers], 200

# Add the resources to the API
api.add_resource(HeroResource, '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers/<int:power_id>')
api.add_resource(HeroesListResource, '/heroes')
api.add_resource(PowersListResource, '/powers')

@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
