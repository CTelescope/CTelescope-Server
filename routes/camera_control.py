"""
    Interfaces de la caméra
"""
from flask import request
from flask_cors import cross_origin
from libraries.camera import *

def init_routes_cmr(app):
    #--------------------------------------------------------
    # Permet d'effectuer un enregistrement video
    @app.route("/api/camera/rafale",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_rafale():
        if request.is_json:
            payload = request.get_json()
            Rafale(Duree=payload["Duree"], FPS = payload["FPS"])
            return {}, 200
        return {"error": "Request must be JSON"}, 415
    
    
    #--------------------------------------------------------
    # Permet d'effectuer un enregistrement video
    @app.route("/api/camera/enregistrement",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_record():
        if request.is_json:
            payload = request.get_json()
            Enregistrement(Duree=payload["Duree"], FPS = payload["FPS"])
            return {}, 200
        return {"error": "Request must be JSON"}, 415
    
    #--------------------------------------------------------
    # Permet d'effectuer un enregistrement video ( start & stop )
    @app.route("/api/camera/enregistrement_start",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_start_record():
        if request.is_json:
            payload = request.get_json()
            StartRecord(FPS = payload["FPS"])
            return {}, 200
        return {"error": "Request must be JSON"}, 415
    
    @app.route("/api/camera/enregistrement_stop",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_stop_record():
        if request.is_json:
            StopRecord()
            return {}, 200
        return {"error": "Request must be JSON"}, 415
    
    #--------------------------------------------------------
    # Permet de prendre des capturesde d'image
    @app.route("/api/camera/captures",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_capture():
        if request.is_json:
            Capture()
            return {}, 200
        return {"error": "Request must be JSON"}, 415