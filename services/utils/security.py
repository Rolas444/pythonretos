from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
str_secret = os.getenv('SECRET_KEY')

def token_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token no encontrado'}), 401
        try:
            data = jwt.decode(token, str_secret, algorithms=['HS256'])
            # current_user = data
        except:
            return jsonify({'message': 'Token inválido'}), 401
        return f( *args, **kwargs)
    return decorated