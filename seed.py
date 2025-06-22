#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance
from datetime import date

with app.app_context():
    print("Deleting data...")
    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()

    print("Creating episodes...")
    ep1 = Episode(date=date(2025, 6, 1), number=1)
    ep2 = Episode(date=date(2025, 6, 2), number=2)
    ep3 = Episode(date=date(2025, 6, 3), number=3)
    episodes = [ep1, ep2, ep3]

    print("Creating guests...")
    guest1 = Guest(name="Oprah Winfrey", occupation="TV Host")
    guest2 = Guest(name="Elon Musk", occupation="Entrepreneur")
    guest3 = Guest(name="Taylor Swift", occupation="Singer")
    guests = [guest1, guest2, guest3]

    print("Creating appearances...")
    app1 = Appearance(episode=ep1, guest=guest1, rating=5)
    app2 = Appearance(episode=ep1, guest=guest2, rating=4)
    app3 = Appearance(episode=ep2, guest=guest3, rating=5)
    app4 = Appearance(episode=ep3, guest=guest1, rating=3)
    appearances = [app1, app2, app3, app4]

    db.session.add_all(episodes)
    db.session.add_all(guests)
    db.session.add_all(appearances)
    db.session.commit()

    print("Seeding complete!")
