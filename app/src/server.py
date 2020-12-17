import os
import glob
import flask
import re
import time
# import json
from flask import Flask, send_from_directory, request, flash, url_for, redirect, render_template, jsonify

from CREATE_DATASET_SET import *
from CREATE_VALIDATION import * 
from MAKE_CLASSIFICATION import * 
from MAKE_VALIDATION import * 
from SET_DONT_CLASS_TO_CLASS import * 

server = flask.Flask(__name__)

UPLOAD_FOLDER = "./VALIDACAO/NAO_CLASSIFICADAS"
CLA_FOLDER = "./VALIDACAO/CLASSIFICADAS"

server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['CLA_FOLDER'] = CLA_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
server.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']



@server.route('/')
def hello():
    return jsonify({"response": "Hello from Docker!"})

@server.route('/file_upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['image']
    foldername = str(int(time.time()))
    filename = foldername+".png"
    file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
    
    # create_validation()
    # make_validation()
    # set_class_label()

    # name = []
    # predict = []
    # for im in glob.glob(CLA_FOLDER+"/*"):
    #     name.append(im)
    #     predict.append(re.findall(r"[@]+[a-z]+",im)[0])
    
    # # send_from_directory(CLA_FOLDER, name[0]+'.png', as_attachment=True)
    # return flask.jsonify({"Classificação": predict[0]})
    return jsonify({"res":"done!"})
   


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5000)
