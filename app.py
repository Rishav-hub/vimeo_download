import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import numpy as np
import json
import datetime
import glob

from src.embed_link import VimeoEmbed

# initialising the flask app
app = Flask(__name__)
CORS(app)
# Creating the upload folder

download_folder = "artifacts/"
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

@app.route('/')
@cross_origin()
def index():
    return render_template('embed.html')

@app.route('/embed_engine', methods=['GET', 'POST'])
@cross_origin()
def embedfile():
    if request.method == 'POST':
        try:

            folder_link = request.form['folder_link'] 
            level = request.form['level']
            cleandir = 'artifacts/'
            for i in glob.glob(cleandir + '*.xlsx'): 
                # del_file = os.path.join(cleandir, i)
                # os.system(f'rm -rf {del_file}')
                os.remove(i)
            obj = VimeoEmbed('secrets/secret.yaml', 'config/config.yaml')
            if level == 'Level 0':
                obj.level_0_embed_link(folder_link)
                # file_name = os.listdir('artifacts')[0]
                # print(file_name)
                # download_folder = f'artifacts/{file_name}'
            elif level == 'Level 1':
                obj.level_1_embed_link(folder_link)
                # file_name = os.listdir('artifacts')[0]
                # download_folder = f'artifacts/{file_name}'
            elif level == 'Level 2':
                obj.level_2_embed_link(folder_link)
                # file_name = os.listdir('artifacts')[0]
                # download_folder = f'artifacts/{file_name}'
            return render_template('embed.html')
        except Exception as e:
            # logging.info("Input format not proper", end= '')
            raise(e)
    else:
        render_template('embed.html')

# displaying the HTML template at the home url
@app.route('/downloader')
def index_1():
   return render_template('download.html')

# Sending the file to the user
@app.route('/download')
def download():
    file_name = os.listdir('artifacts')[0]
    download_folder_1 = f'artifacts/{file_name}'
    return send_file(download_folder_1, as_attachment=True)


if __name__ == '__main__':
    app.run()  # running the flask app
