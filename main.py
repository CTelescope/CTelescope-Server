from pprint import pprint

from camera import Rafale, Enregistrement, Capture
from motor_control import Goto

from flask import Flask, request, jsonify
from flask_cors import cross_origin


""" SETUP FLASK"""
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'

"""
    Permettre de recuperer la position actuellement pointée par le télescope.
"""
@app.route("/api/position",methods=['GET'])
def GetPositionAPI():
    return jsonify({"current_position": '??'})

"""
    Permet d'aller vers une position donnée
"""
@app.route("/api/goto",methods=['POST'])
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
def RecordAPI():
    if request.is_json:
        payload = request.get_json()
        Rafale(Duree=payload["duree_record"], FPS = payload["fps_record"])
        return {'result':f'success'}, 200
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)