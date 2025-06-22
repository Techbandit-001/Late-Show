from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f"<Episode {self.number} on {self.date}>"

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f"<Guest {self.name} - {self.occupation}>"

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))

    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    serialize_rules = ('-guest.appearances', '-episode.appearances')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    def __repr__(self):
        return f"<Appearance {self.rating} stars - Guest {self.guest_id} on Episode {self.episode_id}>"
