from flask import Flask, Blueprint, jsonify, request, render_template
from app.models.all import User, Recipe
from app.utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/")
def index():
    return render_template("index.html")


@recipes_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "user exists"}), 400

    user = User()
    user.username = username
    user.password_hash = generate_password_hash(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "user created"}), 201


@recipes_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "bad credentials"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200


# Create recipe (protected)
@recipes_bp.route("/recipes", methods=["POST"])
@jwt_required()
def create_recipe():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    ingredients = data.get("ingredients")
    instructions = data.get("instructions")

    if not title or not ingredients or not instructions:
        return jsonify({"msg": "title, ingredients and instructions are required"}), 400

    recipe = Recipe()
    recipe.title = title
    recipe.description = description or ""
    recipe.ingredients = ingredients
    recipe.instructions = instructions
    recipe.user_id = user_id

    db.session.add(recipe)
    db.session.commit()

    return jsonify({"msg": "recipe created", "id": recipe.id}), 201


# List all recipes (public)
@recipes_bp.route("/recipes", methods=["GET"])
def list_recipes():
    recipes = Recipe.query.all()
    out = []
    for r in recipes:
        out.append(
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "ingredients": r.ingredients,
                "instructions": r.instructions,
                "user_id": r.user_id,
            }
        )
    return jsonify(out), 200
