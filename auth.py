import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

SECRET = 'football_secret_key'

def generate_token():
    payload = {
        'user': 'admin',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        if token.startswith('Bearer '):
            token = token[7:]
        try:
            jwt.decode(token, SECRET, algorithms=['HS256'])
        except:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated
