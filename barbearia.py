from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['barbearia']
agendamentos = db['agendamentos']

# Rotas de agendamento
@app.route('/agendamentos/', methods=['GET'])
def obter_agendamentos():
    agendamentos_lista = list(agendamentos.find())
    for agendamento in agendamentos_lista:
        agendamento['_id'] = str(agendamento['_id'])
    return jsonify(agendamentos_lista)

@app.route('/agendamentos/', methods=['POST'])
def adicionar_agendamento():
    dados = request.get_json()
    resultado = agendamentos.insert_one(dados)
    return jsonify({'message': 'Agendamento criado com sucesso!', 'id': str(resultado.inserted_id)}), 201

@app.route('/agendamentos/<id>', methods=['DELETE'])
def remover_agendamento(id):
    resultado = agendamentos.delete_one({'_id': ObjectId(id)})
    if resultado.deleted_count > 0:
        return jsonify({'message': 'Agendamento removido com sucesso!'}), 200
    else:
        return jsonify({'message': 'Agendamento não encontrado!'}), 404

@app.route('/agendamentos/<id>', methods=['PUT'])
def editar_agendamento(id):
    dados = request.get_json()
    resultado = agendamentos.update_one({'_id': ObjectId(id)}, {'$set': dados})
    if resultado.modified_count > 0:
        return jsonify({'message': 'Agendamento atualizado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Agendamento não encontrado!'}), 404

if __name__ == '__main__':
    app.run(debug=True)