import os
import glob
import re
import time


from flask import Flask, send_from_directory, request, flash, url_for, redirect, render_template, jsonify

from subprocess import call


app = Flask(__name__)
UPLOAD = "./VALIDACAO/Image"
CLA = "./VALIDACAO/Classificate"

app.config['UPLOAD'] = UPLOAD
app.config['CLA'] = CLA

@app.route('/')
def home():
  return jsonify({"res":"working!"})

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['image']
    foldername = str(int(time.time()))
    filename = foldername+".jpg"
    file.save(os.path.join(app.config['UPLOAD'], filename))
    
    call('python create_data.py',shell = True)
    call('python make_prediction.py',shell = True)
    call('python set_prediction.py',shell = True)

    name = []
    predict = []
    for im in glob.glob(CLA+"/*"):
        name.append(im)
        predict.append(re.findall(r"[@]+[a-zA-Z]+",im)[0][1:])
    
    return jsonify({"Classificacao": predict[0]})
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)






