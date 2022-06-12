"""
    Interfaces de controle du telescope
"""
from flask import jsonify, request
from flask_cors import cross_origin
from astropy.coordinates import SkyCoord
import astropy.units as u

from libraries.control import process_hc_output, goto, get_position, get_motors_speed, set_motors_speed, comp_earth_rot

def init_routes_tls (app):
    #--------------------------------------------------------
    # Permet de recuperer la position actuellement pointée 
    #  par le télescope.
    @app.route("/api/control/position",methods=['GET'])
    def GetPositionAPI():
        return jsonify(get_position())  

    #--------------------------------------------------------
    # Permet de recuperer la position actuellement pointée 
    #  par le télescope.
    @app.route("/api/control/position",methods=['POST'])
    def SetPositionAPI():
        return jsonify({})

    #--------------------------------------------------------
    # Permet de deplacer le telescope vers une position donnée
    # {'AD':'(-+)_:_:_:' Hours Min Sec, 'Dec':'(-+)_:_:_:'} Deg arcMin arcSec
    @app.route("/api/control/goto",methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_goto():
        if request.is_json:
            payload = request.get_json()

            logger.debug(f"{payload['AD']}, {payload['Dec']}")
            
            # WIP
            COORD = SkyCoord(ra='8h50m59.75s', dec='+11d39m22.15s')

            res = goto(COORD)
            
            return {}, 200
        
        else:
            return {"result": "Request must be JSON"}, 415

    #--------------------------------------------------------
    # Permet de deplacer le telescope manuellement
    # exemple : {"AD_steps":0,"DEC_steps":5}
    @app.route("/api/control/hand_controller", methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_hand_controller():
        if request.is_json:
            payload = request.get_json()
            
            if payload.get('AD_hc_output', 0) in [-1,0,1]: 
                AD_hc_output=payload.get('AD_hc_output', 0)
            else: 
                AD_hc_output=0

            if payload.get('DEC_hc_output', 0) in [-1,0,1]: 
                DEC_hc_output=payload.get('DEC_hc_output', 0)
            else: 
                DEC_hc_output=0
                    
            process_hc_output(AD_hc_output, DEC_hc_output)

            return {}, 200
        else:
            return {"result": "Request must be JSON"}, 415

    #--------------------------------------------------------
    # Permet de définir la vitesse des moteurs
    # exemple : {"AD_speed":8,"DEC_steed":0.5}
    @app.route("/api/control/motors_speed", methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_set_speed():
        if request.is_json:
            payload = request.get_json()
            
            AD_speed = payload.get('AD_speed', 0) # Return default value 0 if not found ( 0 == no change )
            DEC_speed = payload.get('DEC_speed', 0) # Return default value 0 if not found ( 0 == no change )
            
            set_motors_speed(AD_speed, DEC_speed)

            return {}, 200
        else:
            return {"result": "Request must be JSON"}, 415

    #--------------------------------------------------------
    # Permet de recuperer la vitesse des deux moteurs
    @app.route("/api/control/motors_speed", methods=['GET'])
    def api_get_motors_speed():
        return jsonify(get_motors_speed())  

    #--------------------------------------------------------
    # Permet l'activation/désativation du mode poursuite
    @app.route("/api/control/tracked_mode", methods=['POST'])
    @cross_origin(supports_credentials=True)
    def api_tracked_mode():
        if request.is_json:

            active = request.get_json()["active"]
            print(active)
            if active in [0,1]:
                comp_earth_rot(active)
                print(active)
                
            
            return {}, 200
        
        return {"result": "Request must be JSON"}, 415