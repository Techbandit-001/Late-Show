from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Episode, Guest, Appearance
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {"message": "Welcome to the Late Show API"}

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        "id": e.id,
        "date": e.date,
        "number": e.number
    } for e in episodes]), 200

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [{
            "id": ap.id,
            "rating": ap.rating,
            "guest_id": ap.guest_id,
            "episode_id": ap.episode_id,
            "guest": {
                "id": ap.guest.id,
                "name": ap.guest.name,
                "occupation": ap.guest.occupation
            }
        } for ap in episode.appearances]
    }), 200

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        "id": g.id,
        "name": g.name,
        "occupation": g.occupation
    } for g in guests]), 200

@app.route('/appearances', methods=['POST'])
def post_appearance():
    data = request.get_json()
    try:
        if not 1 <= data['rating'] <= 5:
            raise ValueError("Rating must be between 1 and 5")

        new_app = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(new_app)
        db.session.commit()

        return jsonify({
            "id": new_app.id,
            "rating": new_app.rating,
            "guest_id": new_app.guest_id,
            "episode_id": new_app.episode_id,
            "episode": {
                "id": new_app.episode.id,
                "date": new_app.episode.date,
                "number": new_app.episode.number
            },
            "guest": {
                "id": new_app.guest.id,
                "name": new_app.guest.name,
                "occupation": new_app.guest.occupation
            }
        }), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    db.session.delete(episode)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
