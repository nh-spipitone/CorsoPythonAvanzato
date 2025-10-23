from flask import request, jsonify, current_app
from models import User
import jwt
from functools import wraps 

def jwt_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token JWT mancante o non valido nell\'intestazione Authorization.'}), 401

        try:
            data = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            current_user_id = data.get('user_id')
            
            user = User.query.get(current_user_id)
            if not user:
                 return jsonify({'message': 'Utente associato al token non trovato.'}), 401
                 
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token JWT scaduto.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token JWT non valido.'}), 401
        except Exception:
            return jsonify({'message': 'Errore durante la decodifica del token.'}), 401
        
        return f(current_user_id, *args, **kwargs)

    return decorated