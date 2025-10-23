from flask import Blueprint, request, jsonify, current_app
from models import User 
import jwt
import datetime
from pydantic import BaseModel, ValidationError

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

class LoginRequest(BaseModel):
    username: str
    password: str

@bp_auth.post("/login")
def login():
    raw_auth_data = request.get_json()

    try:
        validated_data = LoginRequest.model_validate(raw_auth_data)
    except ValidationError as e:
        return jsonify({
            'message': 'Dati di login non validi.',
            'errors': e.errors()
        }), 422

    username = validated_data.username
    password = validated_data.password

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Credenziali non valide.'}), 401

    token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24), 
        'iat': datetime.datetime.now(datetime.UTC)
    }
    
    token = jwt.encode(
        token_payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({
        'token': token, 
        'user_id': user.id,
        'username': user.username
    })

