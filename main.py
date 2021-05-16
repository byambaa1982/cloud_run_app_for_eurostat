import os
from flask import Flask, render_template, request, Response,  send_from_directory, abort, redirect, jsonify, session
import os
import datetime
from google.cloud import storage

from flask import flash, url_for

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]