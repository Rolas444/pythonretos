from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import datetime
from bson.objectid import ObjectId

from database.db import get_db
from routes.todo import todo
from routes.authapi import authapi
from pymongo import MongoClient
from services.utils.security import token_auth

def create_app():
    app = Flask(__name__)
    max_users = 15
    # load_dotenv()
    # stringconnection = os.getenv('MONGO_URI')

    # lista = [("1","uno"), ("2","dos"), ("3","tres")]

    # print(type(lista))

    # clientemongo = MongoClient(stringconnection)

    app.db = get_db()

    usuarios = [usuario for usuario in app.db.usuarios.find({})]


    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/usuarios', methods=['POST','GET'])
    def lista_usuarios():
        if request.method == 'POST':
            username = request.form.get('username')
            parameters = {'name': username}
            # usuarios.append(parameters)
            if len(usuarios) >= max_users:
                return render_template('maxusers.html', max_users=max_users)
            else:    
                app.db.usuarios.insert_one(parameters)
            # print(usuarios)
        return render_template('createusers.html', usuarios=usuarios)
    
    @app.get('/usuarios/<id>')
    def get_user(id):
        user = app.db.usuarios.find_one({'_id': ObjectId(id)})
        if not user:
            return 'usuario no encontrado'
        # print(user)
        return render_template('detailuser.html', user=user)
    
    @app.delete('/usuarios/<id>')
    def delete_user(id):
        app.db.usuarios.delete_one({'_id': id})
        return render_template('createusers.html', usuarios=usuarios)
    
    app.register_blueprint(authapi, url_prefix='/auth')
    app.register_blueprint(todo, url_prefix='/todo')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)