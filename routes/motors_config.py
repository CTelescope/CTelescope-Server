"""
    Interfaces pour le controle les moteurs du telescope
"""
from asyncio import run
from flask import jsonify, request
from flask_cors import cross_origin
from libraries.motor import *

def init_routes_mtrs(app):
    #--------------------------------------------------------
    # 
    # 
    @app.route("/api/SetSpeedAD",methods=['POST'])
    def SetSpeedAD():
        None

    #--------------------------------------------------------
    # 
    # 
    @app.route("/api/SetSpeedDEC",methods=['POST'])
    def SetSpeedDEC():
        None        

    #--------------------------------------------------------
    # 
    # 
    @app.route("/api/GetSpeedAD",methods=['GET'])
    def GetSpeedAD():
        None

    #--------------------------------------------------------
    # 
    # 
    @app.route("/api/GetSpeedDEC",methods=['GET'])
    def GetSpeedDEC():
        None  