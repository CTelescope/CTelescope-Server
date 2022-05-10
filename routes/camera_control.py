"""
    Interfaces de la caméra
"""
from flask import request
from flask_cors import cross_origin
from libraries.camera import *

def init_routes_cmr(app):
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
    # Permet d'effectuer un enregistrement video ( start & stop )
    @app.route("/api/enregistrement_start",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_start_record():
        if request.is_json:
            payload = request.get_json()
            StartRecord(FPS = payload["FPS"])
            return {'result':f'success'}, 200
        return {"error": "Request must be JSON"}, 415
    
    @app.route("/api/enregistrement_stop",methods=['GET'])
    @cross_origin(supports_credentials=True)
    def api_stop_record():
        StopRecord()
        return {'result':f'success'}, 200
    
    #--------------------------------------------------------
    # Permet de prendre des capturesde d'image
    @app.route("/api/captures",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_capture():
        if request.is_json:
            Capture()
            return {'result':f'success'}, 200
        return {"error": "Request must be JSON"}, 415