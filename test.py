import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import numpy as np
import json
import datetime
import glob

from src.embed_link import VimeoEmbed

obj = VimeoEmbed('secrets/secret.yaml', 'config/config.yaml', 'config/video_list.yaml')
obj.level_0_embed_link('https://vimeo.com/manage/folders/6259656')


# https://vimeo.com/manage/folders/11556014