import select
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, People, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)   

"""
    --------Endpoint People--------------------
"""

@api.route("/people", methods=["GET"])
def get_people():
    peopleAll = People.query.all()

    return jsonify(
        [people.serialize() for people in peopleAll]
    ), 201


@api.route("/people/<int:id>", methods=["GET"])
def get_single_person(id):
    single_person = People.query.get(id)

    return jsonify(
        single_person.serialize() 
    ), 201

"""
-----------Endpoint Planet------------------
"""

@api.route("/planet", methods=["GET"])
def get_planets():
    allPlanets = db.session.execute(select(Planet)).scalars().all()


    return jsonify(
        [planet.serialize() for planet in allPlanets]
    ), 201

@api.route("/anet/<int:id>", methods=["GET"])
def get_single_person(id):
    single_planet = Planet.query.get(id)

    return jsonify(
        single_planet.serialize() 
    ), 201


"""
--------Endpoint Favorites----------
"""

"""@app.route("/user/<int:id>/favorites", methods=["POST"])
def add_favorite(id):
    # Obtener el usuario por ID
    user = User.query.get(id)
    
    # Verificar si el usuario existe
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()

    # Verificar que el cuerpo de la solicitud contiene los datos requeridos
    if not data or ("planet_id" not in data and "people_id" not in data):
        return jsonify({"error": "Missing planet_id or people_id"}), 400

    # Crear un nuevo objeto Favorite
    favorite = Favorite(user_id=user.id)

    # Agregar un planeta como favorito si se especifica un planet_id
    if "planet_id" in data:
        planet = Planet.query.get(data["planet_id"])
        if not planet:
            return jsonify({"error": "Planet not found"}), 404
        # Asegurarse de que la relación planet_id se almacene correctamente
        planet_fav = PlanetFavorite(planet_id=planet.id, favorite_id=favorite.id)
        db.session.add(planet_fav)

    # Agregar una persona como favorita si se especifica un people_id
    if "people_id" in data:
        people = People.query.get(data["people_id"])
        if not people:
            return jsonify({"error": "Person not found"}), 404
        # Asegurarse de que la relación people_id se almacene correctamente
        people_fav = PeopleFavorite(peoples_id=people.id, favoritespeople_id=favorite.id)
        db.session.add(people_fav)

    # Guardar el nuevo favorito en la base de datos
    db.session.add(favorite)
    db.session.commit()

    # Retornar el favorito agregado con un estado 201
    return jsonify(favorite.serialize()), 201


@app.route("/user/<int:id>/favorites", methods=["GET"])
def get_user_favorites(id):
    # Obtener el usuario por ID
    user = User.query.get(id)
    
    # Si el usuario no existe, retornar un error
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Obtener los favoritos del usuario
    user_favorites = user.favorites  # Relación con los objetos Favorite

    # Si el usuario no tiene favoritos, retornar un mensaje vacío
    if not user_favorites:
        return jsonify({"message": "No favorites found for this user"}), 200

    # Crear una lista para almacenar los resultados de los favoritos
    serialized_favorites = []

    # Recorrer los favoritos y serializar los planetas y personas
    for favorite in user_favorites:
        # Serializar los planetas
        serialized_planets = [planet.serialize() for planet in favorite.planet_id]
        # Serializar las personas
        serialized_people = [person.serialize() for person in favorite.people_id]

        # Agregar los resultados de cada favorito
        serialized_favorites.append({
            "id": favorite.id,
            "planets": serialized_planets,
            "people": serialized_people
        })

    return jsonify(serialized_favorites), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
"""