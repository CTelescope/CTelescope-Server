"""
    Interfaces pour le controle les moteurs du telescope
"""
from flask import jsonify, request
from flask_cors import cross_origin
from astropy.coordinates import SkyCoord
import astropy.units as u

from libraries.goto import goto, get_position
from libraries.logger import setup_logger, DEBUG

logger = setup_logger(__file__, DEBUG)

def init_routes_tls(app):
    #--------------------------------------------------------
    # Permet de recuperer la position actuellement pointée 
    #  par le télescope.
    @app.route("/api/position",methods=['GET'])
    def GetPositionAPI():
        return jsonify(get_position())

    #--------------------------------------------------------
    # Permet de recuperer la position actuellement pointée 
    #  par le télescope.
    @app.route("/api/position",methods=['POST'])
    def SetPositionAPI():
        return jsonify({})
          
    #--------------------------------------------------------
    # Permet de deplacer le telescope vers une position donnée
    # {'AD':'(-+)_h_m_s', 'Dec':'(-+)_h_m_s'}
    @app.route("/api/goto",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_doSteps():
        if request.is_json:
            payload = request.get_json()
            #logger.debug(f"{payload['AD']}, {payload['Dec']}")
            
            COORD = SkyCoord(ra='8h50m59.75s', dec='+11d39m22.15s')

            res = goto(COORD)
            
            return {}, 200
            # if res[0] == None and res[1] == None:
            #     logger.success("All steps are done !")
            #     return {'status':'done'}, 200
            # else :
            #     logger.failures(f"Something went wrong! ! : {res}")
            #     return {'status':'failed'}, 500
        else:
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