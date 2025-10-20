from flask import Blueprint, jsonify, request
from models import Recipe, db
from helpers import jwt_required
from pydantic import BaseModel, field_validator, Field
from typing import Optional

bp_recipes = Blueprint("recipes", __name__, url_prefix="/recipes")

class RecipeCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    ingredients: str = Field(min_length=1)   
    instructions: str = Field(min_length=1)
    description: Optional[str] = None


    @field_validator('ingredients', 'instructions')
    @classmethod
    def must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("I campi ingredienti e istruzioni non possono essere vuoti.")
        return value


@bp_recipes.get("/")
def get_all_recipes():
    
    all_recipes = Recipe.query.all()

    recipes_list = [recipe.to_dict() for recipe in all_recipes]
    
    return jsonify({
        "message": "Ricette recuperate con successo.",
        "data": recipes_list
    })

@bp_recipes.get("/<int:recipe_id>")
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify({"recipe": recipe.to_dict()})


@bp_recipes.post("/")
@jwt_required 
def create_recipe(current_user_id):
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"message": "Dati ricetta mancanti o incompleti."}), 400
    
    new_recipe = Recipe(
        title=data.get('title'),
        description=data.get('description'),
        ingredients=data.get('ingredients', ''),
        instructions=data.get('instructions', ''),
        user_id=current_user_id 
    )
    
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({
        "message": "Ricetta creata con successo!",
        "recipe": new_recipe.to_dict()
    }), 2