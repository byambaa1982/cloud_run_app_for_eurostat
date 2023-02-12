## Creating Flask APIs in Google Cloud Run 
The code is a Flask API that provides a number of endpoints for various functionalities. It includes the following functionalities:

Retrieving the size of files in a Google Cloud Storage bucket
Retrieving the data from Eurostat API
Transforming an Avro file to a CSV file and uploading it to Google Cloud Storage
Transforming multiple Avro files to multiple CSV files and uploading them to Google Cloud Storage
Hello World endpoint
### Dependencies
The code uses the following libraries:

- Flask: For creating the API
- Google Cloud Storage: For accessing and manipulating files stored in Google Cloud Storage
- Eurostat: A Python wrapper for the Eurostat API
- Pandas: For data manipulation and transformation
- Avro: For reading and writing Avro files
- os: For interacting with the operating system
-Calendar: For formatting dates


### Endpoints


The API has the following endpoints:

- /: A Hello World endpoint
- /sizes: An endpoint that returns the size of files in a Google Cloud Storage bucket
- /unemployment: An endpoint that retrieves data from the Eurostat API based on a keyword passed as a query parameter or in the request body
- /get_data: An endpoint that retrieves data from the Eurostat API and returns a subset of the data as a JSON object
-/avro: An endpoint that accepts a keyword as a query parameter or in the request body, retrieves an Avro file from Google Cloud Storage with that name, transforms it to a CSV file, and uploads the CSV file to Google Cloud Storage
- /multiavro: An endpoint that accepts a list of keywords as a query parameter or in the request body, retrieves Avro files from Google Cloud Storage with those names, transforms each file to a CSV file, and uploads each CSV file to Google Cloud Storage


### How to run the API


To run the API, you need to have Python and the required libraries installed. You also need to have the appropriate credentials to access Google Cloud Storage. Once you have everything set up, you can run the API by executing the following command in the terminal:

Copy code
```python app.py```
The API will be available at http://0.0.0.0:8080/.
