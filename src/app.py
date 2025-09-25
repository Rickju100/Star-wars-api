"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, FavoritePeople, FavoritePlanet
from select import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


"""
-------Endpoint User-------------------
"""

@app.route('/users', methods=['GET'])
def GetAllUsers():
    allUsers = User.query.all()
    return jsonify([user.serialize() for user in allUsers]), 200

@app.route('/users/<int:id>', methods=['GET'])
def GetUsers(id):
    users = User.query.get(id)
    return jsonify(users.serialize()), 200


"""
    --------Endpoint People--------------------
"""

@app.route("/people", methods=["GET"])
def get_people():
    peopleAll = People.query.all()
    return jsonify([people.serialize() for people in peopleAll]), 201


@app.route("/people/<int:id>", methods=["GET"])
def get_single_person(id):
    single_person = People.query.get(id)
    return jsonify(single_person.serialize()), 201


"""
-----------Endpoint Planet------------------
"""

@app.route("/planet", methods=["GET"])
def get_planets():
    allPlanets = Planet.query.all()
    return jsonify([planet.serialize() for planet in allPlanets]), 201


@app.route("/planet/<int:id>", methods=["GET"])
def get_single_planet(id):
    single_planet = Planet.query.get(id)
    return jsonify(single_planet.serialize()), 201

"""
--------Endpoint Favorites----------
"""

@app.route("/favorite/people/<int:id>/", methods=["POST"])
def add_favorite(id):
   

    try:
 
        user_id = 1
     
        favorite = FavoritePeople(user_id=user_id, people_id=id)
        favorite_people = FavoritePeople.query.filter_by(user_id=user_id, people_id=id).first()
        if favorite_people:
            return jsonify({"error":"This people is already on favorites"}), 404

     
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"mensage":"People add to favorite succesfully", 
                        "favorite": favorite.serialize() }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e) } )

@app.route("/favorite/planet/<int:id>/", methods=["POST"])
def add_favorite_planet(id):
   

    try:
 
        user_id = 1
     
        favorite = FavoritePlanet(user_id=user_id, planet_id=id)
        favorite_planet= FavoritePlanet.query.filter_by(user_id=user_id, planet_id=id).first()
        if favorite_planet:
            return jsonify({"error":"This people is already on favorites"}), 404

     
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"mensage":"Planet added to favorite succesfully", 
                        "favorite": favorite.serialize() }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e) } )

@app.route("/users/favorites", methods=["GET"])
def get_favorites():
    user_id = 1
    favorite_people = FavoritePeople.query.all()
    favorite_planet = FavoritePlanet.query.all()

    favorites = {
        "people": [fav.serialize() for fav in favorite_people],
        "planets": [fav.serialize() for fav in favorite_planet]
    }
    return jsonify(favorites), 200        

@app.route("/favorite/people/<int:id>/", methods=["DELETE"])
def delete_favorite(id):
    user_id = 1
    favorite_people = FavoritePeople.query.filter_by(user_id=user_id, people_id=id).first()
    if not favorite_people:
        return jsonify({"error":"This people is not on favorites"}), 404
    db.session.delete(favorite_people)
    db.session.commit()
    return jsonify({"mensage":"Favorite deleted succesfully"}), 200  
    
@app.route("/favorite/planet/<int:id>/", methods=["DELETE"])
def delete_favorite_planet(id):
    user_id = 1
    favorite_planet = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=id).first()
    if not favorite_planet:
        return jsonify({"error":"This planet is not on favorites"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"mensage":"Favorite deleted succesfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
