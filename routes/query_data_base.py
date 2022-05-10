"""
    Interfaces pour les requetes vers la BDD
"""
from flask import jsonify, request
from libraries.BDD import *

def init_routes_db(app):
    #--------------------------------------------------------
    # Permet de récuperer la liste des objets
    @app.route('/api/objets', methods = ['GET'])
    def api_get_objects():
        return jsonify(get_objects())

    #-------------------------------------------------------
    # Permet de récuperer un objet par sont Id
    @app.route('/api/objet/<Id_obj>', methods = ['GET'])
    def api_get_object(Id_obj):
        return jsonify(get_object_by_id(Id_obj))

    #--------------------------------------------------------
    # Permet d'ajouter un objet
    @app.route('/api/objet/add', methods = ['POST'])
    def api_add_object():
        objet = request.get_json()
        return jsonify(insert_object(objet))

    #--------------------------------------------------------
    # Permet de mettre a jour la liste d'objets
    @app.route('/api/objet/update', methods = ['PUT'])
    def api_update_object():
        objet = request.get_json()
        return jsonify(update_object(objet))
    #--------------------------------------------------------
    # Permet de mettre a jour un objet avec son Id
    @app.route('/api/objet/delete/<Id_obj>', methods = ['DELETE'])
    def api_delete_object(Id_obj):
        return jsonify(delete_object(Id_obj))

    #--------------------------------------------------------
    # Permet de récuperer la listes des constellations
    @app.route('/api/constellations', methods = ['GET'])
    def api_get_consts():
        return jsonify(get_constellations())

    #--------------------------------------------------------
    # Permet de récuperer une constellations par sont Id
    @app.route('/api/constellation/<Id_const>', methods = ['GET'])
    def api_get_const(Id_const):
        return jsonify(get_const_by_id(Id_const))

    #--------------------------------------------------------
    # Permet de récuperer la listes des types
    @app.route('/api/types', methods = ['GET'])
    def api_get_types():
        return jsonify(get_types())

    #--------------------------------------------------------
    # Permet de récuperer un type par sont Id
    @app.route('/api/type/<Id_type>', methods = ['GET'])
    def api_get_type(Id_type):
        return jsonify(get_type_by_id(Id_type))