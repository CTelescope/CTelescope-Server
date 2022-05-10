"""
    Interfaces pour le controle les moteurs du telescope
"""
from asyncio import run
from flask import jsonify, request
from flask_cors import cross_origin
from libraries.motors import *

def init_routes_mtrs(app):
    #--------------------------------------------------------
    # Permet de recuperer la position actuellement pointée 
    #  par le télescope.
    @app.route("/api/position",methods=['GET'])
    def GetPositionAPI():
        return jsonify({"current_position": '??'})

    #--------------------------------------------------------
    # Permet de deplacer le telescope vers une position donnée
    @app.route("/api/doSteps",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_doSteps():
        if request.is_json:
            payload = request.get_json()
            #goto(payload["nb_steps"])
            res = run(goto(NB_STEPS_MOTEUR_AD = 2400, NB_STEPS_MOTEUR_DEC = -2400))
            return {'result':'done'}, 200
        return {"result": "Request must be JSON"}, 415

    #--------------------------------------------------------
    # Permet de deplacer le telescope vers une position donnée
    @app.route("/api/trackedMode",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_trackedMode():
        if request.is_json:
            tracked = request.get_json()["tracked"]

            return {'result':'done'}, 200
        return {"result": "Request must be JSON"}, 415