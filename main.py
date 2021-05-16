import os
from flask import Flask, render_template, request, Response,  send_from_directory, abort, redirect, jsonify, session
import os
import datetime
from google.cloud import storage

from flask import flash, url_for

from os import getenv
import pandas as pd
from flask import jsonify
import eurostat

app = Flask(__name__)

client = storage.Client()
bucket_name='getting-termites-tweet'
bucket = client.get_bucket(bucket_name)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route('/sizes')
def get_size(bucket_name='getting-termites-tweet'):
    data=[]
    for blob in client.list_blobs(bucket_name): 
        data_size=('{:.1f}'.format(blob.size/1000))
        update_date=('{}'.format(blob.updated))
        mydic={"file":blob.name, "size":data_size, "updates":update_date[0:10]}
        data.append(mydic)
    return jsonify(data)

@app.route('/heads')
def get_eurostat_data(request):

  #------ Get Search word here---
  request_json = request.get_json() 
  request_args = request.args 
  key_word = "" 

  if request_json and 'key_word' in request_json: 
    key_word = request_json['key_word'] 
  elif request_args and 'key_word' in request_args: 
    key_word = request_args['key_word']
  code=key_word
  print(code)
  #--------------------------------
  try:
    df = eurostat.get_data_df(code)
    print('code:{} columns:{} rows:{}'.format(code, df.shape[1], df.shape[0]))
  except: 
    df='{} not found in the Eurostat server'.format(code)
    print('{} not found in the Eurostat server'.format(code))


  return jsonify(df.head)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]