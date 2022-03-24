#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from camera import Rafale, Enregistrement, Capture
from motor_control import Goto
from BDD import get_objects,get_object_by_id,update_object,delete_object,get_constellations,get_const_by_id,get_types,get_type_by_id,insert_object

""" 
    FLASK SETUP 
"""
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
CORS(app, support_credentials=True)

"""
    Interfaces pour le controle des moteurs du telescope
"""
#--------------------------------------------------------
# Permet de recuperer la position actuellement pointée 
#  par le télescope.
@app.route("/api/position",methods=['GET'])
@cross_origin(supports_credentials=True)
def GetPositionAPI():
    return jsonify({"current_position": '??'})

#--------------------------------------------------------
# Permettre de recuperer la position actuellement pointée 
#  par le télescope.
@app.route("/api/goto",methods=['POST'])
@cross_origin(supports_credentials=True)
def api_goto():
    if request.is_json:
        payload = request.get_json()
        Goto(payload["mode"], payload["nb_steps"])
        return {'new position':f'???'}, 200
    return {"error": "Request must be JSON"}, 415


"""
    Interfaces de la caméra
"""
#--------------------------------------------------------
# Permet d'effectuer un enregistrement video
@app.route("/api/rafales",methods=['POST'])
@cross_origin(supports_credentials=True)
def api_rafale():
    if request.is_json:
        payload = request.get_json()
        Rafale(Duree=payload["duree"], FPS = payload["fps"])
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415


#--------------------------------------------------------
# Permet d'effectuer un enregistrement video
@app.route("/api/enregistrement",methods=['POST'])
@cross_origin(supports_credentials=True)
def api_record():
    if request.is_json:
        payload = request.get_json()
        Enregistrement(Duree=payload["duree_record"], FPS = payload["fps_record"])
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415

#--------------------------------------------------------
# Permet de prendre des capturesde d'image
@app.route("/api/captures",methods=['POST'])
@cross_origin(supports_credentials=True)
def api_capture():
    if request.is_json:
        Capture()
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415


"""
    Interfaces pour les requetes vers la BDD
"""
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

# Entry point
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)