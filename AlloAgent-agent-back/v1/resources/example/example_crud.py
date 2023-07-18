# pylint: disable=invalid-name
# pylint: disable=line-too-long
#imports python base
import json
import logging
import pymongo
#import terceros
from flask import session, jsonify
from flask_restful import Resource, reqparse
from mongoengine.context_managers import switch_db

#Import del sistema
from v1.resources.auth.authorization import Auth
from v1.resources.auth.dbDecorator import dbAccess
from v1.models.api_models import Model1

logger = logging.getLogger(__name__)

class Model1_CRUD(Resource): #Clase para crear recursos REST
    # @Auth.authenticate
    # @dbAccess.mongoEngineAccess
    # def get(self):
    #     parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
    #     parser.add_argument("name", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("lastname", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("user", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("adress", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("email", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("rol", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("document_type", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("document_number", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     parser.add_argument("phone", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
    #     data = parser.parse_args() #obtenemos los datos de la request

    #     with switch_db(Model1, session["dbMongoEngine"]):
    #         my_model = Model1.objects(name=data['name']).first()
    #         my_model = Model1.objects(surname=data['lastname'])
    #         my_model = Model1.objects(username=data['user'])
    #         my_model = Model1.objects(adress=data['adress'])
    #         my_model = Model1.objects(mail=data['email'])
    #         my_model = Model1.objects(role=data['rol'])
    #         my_model = Model1.objects(TypeDocument=data['document_type'])
    #         my_model = Model1.objects(numberDocument=data['document_number'])
    #         my_model = Model1.objects(phone=data['phone'])
    #         if my_model:
    #            return jsonify(my_model.to_json()) 
    #     return "Objeto no encontrado", 400

    
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        with switch_db(Model1, session["dbMongoEngine"]):
            my_model = Model1.objects()
            if my_model:
                return jsonify(my_model.to_json())
        return "Objeto no encontrado", 400

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self): #Se ejecutara este metodo con el metodo post del endpoint
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("name", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("lastname", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("document_type", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("document_number", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("rol", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado") 
        parser.add_argument("user", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("password", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("address", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("email", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("phone", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")  
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(Model1, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(document_number=data['document_number']).first()
            my_obj = my_obj(
                name=data['name'], 
                lastname=data['lastname'], 
                document_type=data['document_type'], 
                document_number=data['document_number'],
                rol=data['rol'],
                user=data['user'], 
                password=data['password'], 
                address=data['address'], 
                email=data['email'],
                phone=data['phone']
            )
            # my_model = Model1.objects(name=data['name'])
            # my_model = Model1.objects(surname=data['lastname'])
            # my_model = Model1.objects(TypeDocument=data['document_type'])
            # my_model.numberDocument = data['document_number']
            # my_model = Model1.objects(role=data['rol'])
            # my_model = Model1.objects(username=data['user'])
            # my_model = Model1.objects(password=data['password'])
            # my_model = Model1.objects(address=data['adress'])
            # my_model = Model1.objects(mail=data['email'])
            # my_model.phone = data['phone']
            my_obj.save()
        return jsonify(my_obj.to_json())

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def put(self):
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("name", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("lastname", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("document_type", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("document_number", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("rol", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("user", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("password", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("address", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("email", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("phone", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        try:
            with switch_db(Model1, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(name=data['name'], 
                lastname=data['lastname'], 
                document_type=data['document_type'], 
                document_number=data['document_number'],
                rol=data['rol'],
                user=data['user'], 
                password=data['password'], 
                address=data['address'], 
                email=data['email'],
                phone=data['phone'])
                my_model.save()
        except Exception as err:
            logger.error(err)
        return jsonify(my_model.to_json())

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        parser = reqparse.RequestParser() #creamos un objeto para obtener los datos de la request
        parser.add_argument("document_number", type=int, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #obtenemos los datos de la request

        with switch_db(Model1, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(document_number=data['document_number']).first()
            if not my_obj:
                return jsonify({'error': 'data not found'})
            my_obj.delete()
        return "Ok", 200

    #documentacion sobre requestParser https://flask-restful.readthedocs.io/en/latest/reqparse.html
    #documentacion sobre decoradores https://github.com/alloxentric/KeycloakAuth
    #docuemntacion sobre flask https://flask.palletsprojects.com/en/2.0.x/
    #documentacion sobre flask restful https://flask-restful.readthedocs.io/en/latest/
