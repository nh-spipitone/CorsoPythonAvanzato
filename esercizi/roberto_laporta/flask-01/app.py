from dataclasses import asdict, dataclass
from flask import Flask, jsonify, request

from typing import List

app = Flask(__name__)

@dataclass
class Ricetta:
    id: int 
    nome: str
    ingredienti: List[str]
    tempo_preparazione: int 


frittata = Ricetta(
    id=1,
    nome="Frittata",
    ingredienti=["Uova", "Olio", "Sale"],
    tempo_preparazione=5
)


ricette:List[Ricetta] = [frittata]


@app.route('/api/ricette/<int:ricetta_id>', methods=['GET'])
def getRicettaById(ricetta_id: int):
    ricetta_esistente = next((elemento for elemento in ricette if elemento.id == ricetta_id), None)
    if ricetta_esistente:
        return jsonify(ricetta_esistente)
    else:
        return jsonify({"messaggio": f"Ricetta con ID {ricetta_id} non trovata."}), 404



@app.route('/api/ricette/all', methods=['GET'])
def getAllRicette():
    return ricette



@app.route('/api/ricette', methods=['POST'])
def createRicetta():
    body:Ricetta = request.get_json()

    campi_richiesti = ['id','nome', 'ingredienti', 'tempo_preparazione']

    for campo in campi_richiesti:
        if campo not in body:
            return jsonify({"errore": f"Campo mancante: '{campo}'"}), 400

    nuova_ricetta=Ricetta(**body)

    ricetta_dict = asdict(nuova_ricetta)
    ricette.append(ricetta_dict)

    return ricetta_dict


app.run()
    

