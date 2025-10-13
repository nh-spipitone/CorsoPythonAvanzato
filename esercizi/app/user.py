from typing import Any

from flask import Blueprint, abort, request
from pydantic import BaseModel, PositiveInt


bp = Blueprint("user", "user", url_prefix="/user")
cache: dict[int, Any] = {}
current_user_id: int = 0


@bp.route("/<int:user_id>", methods=("GET",))
def get_user(user_id: int) -> tuple[dict[str, Any], int]:
    if user_id not in cache:
        abort(404)
    
    return cache[user_id], 200


class UserPayload(BaseModel):
    username: str
    eta: PositiveInt


@bp.route("/", methods=("POST",))
def post_user() -> tuple[dict[str, Any], int]:
    username = request.form.get("username")
    eta = request.form.get("eta")
    
    try:
        user = UserPayload(username=username, eta=eta)
    except:
        return abort(400)

    global current_user_id
    current_user_id += 1
    obj: dict[str, Any] = {
        "user_id": current_user_id,
        "username": user.username,
        "eta": user.eta,
    }
    cache[current_user_id] = obj
    return obj, 201
