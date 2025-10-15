from typing import Any

from flask import Blueprint, abort, request
from pydantic import BaseModel, PositiveInt


bp = Blueprint("user", "user", url_prefix="/user")


@bp.route("/<int:student_id>", methods=("GET",))
def get_student(student_id: int) -> tuple[dict[str, Any], int]:
    cur = bp.conn.cursor()
    cur.execute("SELECT * FROM studente WHERE id = %s", (student_id,))
    data = cur.fetchone()
    cur.close()

    return {
        "id": data[0],
        "name": data[1],
        "surname": data[2],
        "age": data[3],
        "email": data[4],
    }, 200


class StudentPayload(BaseModel):
    name: str
    surname: str
    age: PositiveInt | None
    email: str | None


@bp.route("/", methods=("POST",))
def post_user() -> tuple[dict[str, Any], int]:
    try:
        print(request.form)
        student = StudentPayload(
            name=request.form.get("name"),
            surname=request.form.get("surname"),
            age=request.form.get("age"),
            email=request.form.get("email"),
        )
    except:
        return abort(400)

    cur = bp.conn.cursor()
    cur.execute("INSERT INTO studente (nome, cognome, eta, email) VALUES (%s, %s, %s, %s) RETURNING id", (
        student.name,
        student.surname,
        student.age,
        student.email,
    ))
    s_id = cur.fetchone()
    bp.conn.commit()
    cur.close()
    obj: dict[str, Any] = {
        "id": s_id[0],
        "name": student.name,
        "surname": student.surname,
        "age": student.age,
        "email": student.email,
    }
    return obj, 201









