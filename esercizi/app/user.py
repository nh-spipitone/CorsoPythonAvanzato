from typing import Any, Literal

from flask import Blueprint, abort, request


bp = Blueprint("user", "user", url_prefix="/user")
cache: dict[int, Any] = {}
current_user_id: int = 0


@bp.route("/<int:user_id>", methods=("GET",))
def get_user(user_id: int) -> tuple[dict[str, Any], int]:
    if user_id not in cache:
        abort(404)
    
    return cache[user_id], 200


@bp.route("/", methods=("POST",))
def post_user() -> tuple[dict[str, Any], int]:
    username = request.form.get("username")
    eta = request.form.get("eta")
    if not username or not eta:
        abort(400)

    current_user_id += 1
    obj: dict[str, Any] = {
        "user_id": current_user_id,
        "username": username,
        "eta": eta,
    }
    cache[current_user_id] = obj
    return obj, 201
