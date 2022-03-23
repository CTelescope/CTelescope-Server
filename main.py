from pprint import pprint

from camera import Rafale, Enregistrement, Capture
from motor_control import Goto
from BDD import get_objects,get_object_by_id,update_object,delete_object,get_constellations,get_const_by_id,get_types,get_type_by_id,insert_object

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin





""" SETUP FLASK"""
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
CORS(app, support_credentials=True)

"""
    Permettre de recuperer la position actuellement pointée par le télescope.
"""
@app.route("/api/position",methods=['GET'])
@cross_origin(supports_credentials=True)
def GetPositionAPI():
    return jsonify({"current_position": '??'})

"""
    Permet d'aller vers une position donnée
"""
@app.route("/api/goto",methods=['POST'])
@cross_origin(supports_credentials=True)
def GotoAPI():
    if request.is_json:
        payload = request.get_json()
        Goto(payload["mode"], payload["nb_steps"])
        return {'new position':f'???'}, 200
    return {"error": "Request must be JSON"}, 415

"""
    Permet ...
"""
@app.route("/api/rafales",methods=['POST'])
@cross_origin(supports_credentials=True)
def RafaleAPI():
    if request.is_json:
        payload = request.get_json()
        Rafale(Duree=payload["duree"], FPS = payload["fps"])
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415


"""
    Permet ...
"""
@app.route("/api/enregistrement",methods=['POST'])
@cross_origin(supports_credentials=True)
def RecordAPI():
    if request.is_json:
        payload = request.get_json()
        Enregistrement(Duree=payload["duree_record"], FPS = payload["fps_record"])
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415

"""
    Permet ...
"""
@app.route("/api/captures",methods=['POST'])
@cross_origin(supports_credentials=True)
def CapturesAPI():
    if request.is_json:
        Capture()
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415


"""
    Permet ...
"""
#Objet
@app.route('/api/objets', methods = ['GET'])
def api_get_objects():
    return jsonify(get_objects())

"""
    Permet ...
"""

@app.route('/api/objet/<Id_obj>', methods = ['GET'])
def api_get_object(Id_obj):
    return jsonify(get_object_by_id(Id_obj))

"""
    Permet ...
"""
@app.route('/api/objet/add', methods = ['POST'])
def api_add_object():
    objet = request.get_json()
    return jsonify(insert_object(objet))

"""
    Permet ...
"""
@app.route('/api/objet/update', methods = ['PUT'])
def api_update_object():
    objet = request.get_json()
    return jsonify(update_object(objet))

"""
    Permet ...
"""

@app.route('/api/objet/delete/<Id_obj>', methods = ['DELETE'])
def api_delete_object(Id_obj):
    return jsonify(delete_object(Id_obj))

#Constellation
@app.route('/api/constellations', methods = ['GET'])
def api_get_consts():
    return jsonify(get_constellations())

@app.route('/api/constellation/<Id_const>', methods = ['GET'])
def api_get_const(Id_const):
    return jsonify(get_const_by_id(Id_const))

"""
    Permet ...
"""


#Type
@app.route('/api/types', methods = ['GET'])
def api_get_types():
    return jsonify(get_types())

"""
    Permet ...
"""

@app.route('/api/type/<Id_type>', methods = ['GET'])
def api_get_type(Id_type):
    return jsonify(get_type_by_id(Id_type))





    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
