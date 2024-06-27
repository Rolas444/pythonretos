from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime
import os
from dotenv import load_dotenv
from database.db import get_db

conection = get_db()
users = conection.users
load_dotenv()
str_secret = os.getenv('SECRET_KEY')

authapi = Blueprint('authapi', __name__)

@authapi.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    username, password = data['username'], data['password']
    if(password == ''):
        return jsonify({'message': 'La contraseña no puede estar vacía'}), 400
    dbuser = conection.users.find_one({'name': username})
    if dbuser:
        return jsonify({'message': 'El usuario ya existe'}), 400
    hashed_password = generate_password_hash(password)
    users.insert_one({'name': username, 'password': hashed_password})
    return jsonify({'message': 'Usuario creado'}), 201
        
@authapi.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username, password = data['username'], data['password']
    dbuser = conection.users.find_one({'name': username})
    if not dbuser:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    if not check_password_hash(dbuser['password'], password):
        return jsonify({'message': 'Contraseña incorrecta'}), 400
    token = jwt.encode({'username': data['username'], 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60)}, str_secret)
    return jsonify({'token': token}), 200

