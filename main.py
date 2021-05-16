from flask import Flask, render_template, request, Response,  send_from_directory, abort, redirect, jsonify, session
import os
from google.cloud import storage
from flask import flash, url_for
from os import getenv
import pandas as pd
from flask import jsonify
import eurostat
from datetime import datetime
from io import StringIO
from io import BytesIO
import os
import calendar
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

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

@app.route('/unemployment')
def get_eurostat_data():
	code='unemployment'
	#--------------------------------
	try:
		toc_df = eurostat.get_toc_df()
		df = eurostat.subset_toc_df(toc_df, 'unemployment')
		# df = eurostat.get_data_df(code)
		print('code:{} columns:{} rows:{}'.format(code, df.shape[1], df.shape[0]))
		data=df.shape[0]
	except: 
		df='{} not found in the Eurostat server'.format(code)
		print('{} not found in the Eurostat server'.format(code))
		return jsonify(df)
	return jsonify(data)

@app.route('/avro', methods = ['GET', 'POST'])
def check_and_trans_by_http():
	#------ storage link here---
	try:
		request_json = request.get_json() 
		request_args = request.args 
		key_word = "" 

		if request_json and 'key_word' in request_json: 
			key_word = request_json['key_word'] 
		elif request_args and 'key_word' in request_args: 
			key_word = request_args['key_word']
			fname=key_word
		print(fname)
		client = storage.Client()
		#please change the file's URI
		myurl=str(fname)
		bucket=client.get_bucket('getting-termites-tweet')
		if '.avro' in myurl:
			# blob=bucket.blob(my_file)
			blob=bucket.blob(fname)
			blob.download_to_filename("/tmp/temp.avro")
			reader = DataFileReader(open("/tmp/temp.avro", "rb"), DatumReader())
			records = [r for r in reader]
			# Populate pandas.DataFrame with records
			df = pd.DataFrame.from_records(records)
			print('url is {}'.format(myurl))
			print('chunk shape is {}'.format(df.shape))
			date_until=datetime.today().strftime('%Y-%m-%d')
			filename=('test_v7_{}.csv'.format(date_until))
			print(filename)
			f = StringIO()
			df2=df[['ip_address', 'date_time','advertiser_id','line_item_id','event_type']]
			df2['temp_date']=df2.date_time.map(lambda x:datetime.fromtimestamp(x))
			df2['Timestamp']=df2.temp_date.map(lambda my_date: '{}, {}'.format(calendar.day_name[my_date.weekday()], my_date.strftime("%b %d, %Y")))
			df2=df2[['ip_address', 'Timestamp','date_time','advertiser_id','line_item_id','event_type']]
			df2.to_csv(f, index=False)
			f.seek(0)
			client=storage.Client()
			newbucket=client.get_bucket('my-image-data-bucket-2021')
			newblob=newbucket.blob(filename)
			newblob.upload_from_string(f.read(), content_type='text/csv')
			print('uploaded storage')
		else: 
			print('no avro file found')
		return f'check the results in the logs'
	except:
		data="something wrong, nothin happend"
		return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]