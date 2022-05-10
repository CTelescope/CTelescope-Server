"""
    Interfaces pour la gallerie
"""
from re import sub
from flask import send_file
from glob import glob
from os import path

captures_files_dir = []   #[] glob("gallery/captures/*.jpg")
records_files_dir  = []   #glob("gallery/enregistrement/*.jpg")
rafales_files_dir  = []   #glob("gallery/rafales/*/*.jpg")

def init_media_files_dir():
    global captures_files_dir
    global records_files_dir
    global rafales_files_dir
    
    captures_files_dir = glob("gallery/captures/*.jpg")
    records_files_dir = glob("gallery/enregistrement/*.jpg")
    rafales_files_dir = []
    
    for sub_rafale_file in  glob("gallery/rafales/*"):
        rafales_images = glob(path.join(sub_rafale_file,"/*.jpg"))
        rafales_files_dir.append[sub_rafale_file, rafales_images]


def init_routes_glr(app):
    @app.route('/api/gallery/get_captures')
    def get_captures():
        test = glob("gallery/captures/*.jpg")
        return send_file(test, mimetype='image/jpg')
    
    # TOTO : Get tree