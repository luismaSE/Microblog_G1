from flask_restful import Resource
from flask import request, jsonify, session, Response
from .. import mongo
from bson import json_util
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Resource):

    def get(self, alias):
        user = mongo.db.users.find_one({'alias': alias, })
        response = json_util.dumps(user)
        return Response(response, mimetype="application/json")

    @jwt_required()
    def put(self, alias):
        user = mongo.db.users.find_one({"alias": alias})        
        if user is None:
            return "Usuario inexistente", 404
        
        claims = get_jwt()
        usuario = claims["alias"]
        
        if usuario == alias:
            return "No te podes autoseguir.", 404
        
        mongo.db.users.update_one({"alias": alias},{'$push': {'seguidores': usuario}})
        mongo.db.users.update_one({"alias": usuario}, {'$push': {'seguidos': alias}})

        return "Comenzaste a seguir a '{}'".format(alias), 201


    # @app.route('/users/<id>', methods=['DELETE'])
    # def delete_user(id):
    #     mongo.db.users.delete_one({'_id': ObjectId(id)})
    #     response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    #     response.status_code = 200
    #     return response


    # @app.route('/users/<_id>', methods=['PUT'])
    # def update_user(_id):
    #     username = request.json['username']
    #     email = request.json['email']
    #     password = request.json['password']
    #     if username and email and password and _id:
    #         hashed_password = generate_password_hash(password)
    #         mongo.db.users.update_one(
    #             {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
    #         response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
    #         response.status_code = 200
    #         return response
    #     else:
    #         return not_found()
        
class Usuarios(Resource):

    def get(self):
        users = mongo.db.users.find()
        response = json_util.dumps(users)
        return Response(response, mimetype="application/json")


class UsuariosEncontrados(Resource):

    def get(self, alias):
        user = mongo.db.users.find({'alias': {'$regex': alias, '$options': 'i'}})
        response = json_util.dumps(user)
        return Response(response, mimetype="application/json")
