from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    
    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete')

    # Serialization rules
    serialize_rules = ('-hero_powers',)  # Exclude hero_powers

    @validates('name', 'super_name')
    def validate_fields(self, key, value):
        if not value or len(value) > 50:
            raise ValueError(f'{key.capitalize()} must be non-empty and less than 50 characters')
        return value

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete')

    # Serialization rules
    serialize_rules = ('-hero_powers.power',)  # Exclude hero_powers

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) > 50:
            raise ValueError('Name must be non-empty and less than 50 characters')
        return name

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) > 200:
            raise ValueError('Description must be non-empty and less than 200 characters')
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # Serialization rules
    serialize_rules = ('-hero', '-power')  # Exclude relationships

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Strength must be Strong, Weak, or Average')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
