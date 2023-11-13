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
from models import db, User, Characters, Planets
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

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = db.session.execute(db.select(User).order_by(User.name)).scalars()
        result = [item.serialize() for item in users]
        response_body = {"message":"GET de todos los usuarios",
                        "status": "OK",
                        "Users": result}
        return response_body, 200
    if request.method == 'POST':
        request_body = request.get_json()
        user = User(name = request_body["name"],
                    email = request_body["email"],
                    password = request_body["password"])
        db.session.add(user)
        db.session.commit()
        response_body = {"message": "New user add",
                         "Status": "OK",
                         "New user": request_body}
        return response_body, 200


@app.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
def handle_user(id):
    if request.method == 'GET':
        user = db.get_or_404(User, id)
        response_body = {"message": "Devuelve el usuario segun su ID",
                         "status": "OK",
                         "response": user.serialize()}
        return response_body, 200
    if request.method == 'PUT':
        request_body = request.get_json()
        user = db.get_or_404(User, id)
        user.email = request_body["email"]
        user.name = request_body["name"]
        user.password = request_body["password"]    
        db.session.commit()
        response_body = {"message": "User update",
                         "status": "OK",
                        "response": request_body}
        return response_body, 200
    if request.method == 'DELETE':
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
        response_body = {"message": "User delete",
                         "status": "OK",
                         "User delete": id
                         }
        return response_body,200
    

@app.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    if request.method == 'GET':
        characters = db.session.execute(db.select(Characters).order_by(Characters.name)).scalars()
        result = [item.serialize() for item in characters]
        response_body = {"message": "GET de todos los characters",
                         "status": "OK",
                         "response": result}
        return response_body, 200
    if request.method == 'POST':
        request_body = request.get_json()
        character = Characters(url = request_body["url"],
                               name = request_body["name"])
        db.session.add(character)
        db.session.commit()
        response_body = {"message": "New user created",
                         "status": "OK",
                         "response": request_body}
        return response_body, 200
    

@app.route('/characters/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_character(id):
    if request.method == 'GET':
        character = db.get_or_404(Characters, id)
        responce_body = {"message": "Character optenido por el ID",
                         "status": "OK",
                         "response": character.serialize()}
        return responce_body, 200
    if request.method == 'PUT':
        request_body = request.get_json()
        character = db.get_or_404(Characters, id)
        character.url = request_body["url"]
        character.name = request_body["name"]
        db.session.commit()
        response_body = {"message": "Character update",
                         "status": "OK",
                         "response": request_body}
        return response_body, 200
    if request.method == 'DELETE':
        character = db.get_or_404(Characters, id)
        db.session.delete(character)
        db.session.commit()
        response_body = {"message": "Character delete",
                         "status": "OK",
                         "Character delete": id}
        return response_body, 200
    

@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        planets = db.session.execute(db.select(Planets).order_by(Planets.name)).scalars()
        result = [item.serialize() for item in planets]
        response_body = {"message": "GET de todos los planets",
                         "status": "OK",
                         "response": result}
        return response_body, 200
    if request.method == 'POST':
        request_body = request.get_json()
        planet = Planets(url = request_body["url"],
                            name = request_body["name"])
        db.session.add(planet)
        db.session.commit()
        response_body = {"message": "New planet created",
                         "status": "OK",
                         "response": request_body}
        return response_body, 200
    

@app.route('/planets/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_planet(id):
    if request.method == 'GET':
        planet = db.get_or_404(Planets, id)
        responce_body = {"message": "Planet optenido por el ID",
                         "status": "OK",
                         "response": planet.serialize()}
        return responce_body, 200
    if request.method == 'PUT':
        request_body = request.get_json()
        planet = db.get_or_404(Planets, id)
        planet.url = request_body["url"]
        planet.name = request_body["name"]
        db.session.commit()
        response_body = {"message": "Planet update",
                         "status": "OK",
                         "response": request_body}
        return response_body, 200
    if request.method == 'DELETE':
        planet = db.get_or_404(Planets, id)
        db.session.delete(planet)
        db.session.commit()
        response_body = {"message": "Planet delete",
                         "status": "OK",
                         "Planet delete": id}
        return response_body, 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
