"""
    Interfaces pour la gallerie
"""
from flask import send_file

def init_routes_glr(app):
    @app.route('/get_image')
    def get_image():
        filename = 'test.jpg'
        return send_file(filename, mimetype='image/jpg')
    
    # TOTO : Get tree