from flask import Flask, render_template, request
import os
import datetime

from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    clientemongo = MongoClient(os.getenv('MONGO_URI'))

    app.db = clientemongo.pythonapp

    usuarios = [usuario for usuario in app.db.usuarios.find({})]


    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/usuarios', methods=['POST','GET'])
    def lista_usuarios():
        if request.method == 'POST':
            username = request.form.get('username')
            parameters = {'name': username}
            usuarios.append(parameters)
            app.db.usuarios.insert_one(parameters)
            # print(usuarios)
        return render_template('createusers.html', usuarios=usuarios)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()