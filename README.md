# Projet Fil Rouge

Projet Fil Rouge is a REST API using : 

  - Python
  - Flask
 
 This API was designed to complete the Fil rouge project of MS SIO. The goal of this API is to retrieve the metadata (name, mimetype, and size) of an input file associated to the data  present in the file. For the moment, only those mimetypes are supported : *.txt*, *.csv* ( "," must be the delimiter),  *.jpg*, *.jpeg* , *.pdf*, *.png* .
The API send back the metadata and data in a json. To see more and to use it, please follow the following steps : 


## Getting started

### Prerequesites
You need to have : 
* 3.7 python installed : https://www.python.org/downloads/release/python-370/

* Pipenv installed : 
```sh
# Install pipenv
$ pip3 install pipenv
```
See as well the [Pipenv documentation] which is the package manager that I have used in this project.

### Installation
Clone the repository 
```sh
# Clone the repo
$ git clone https://github.com/Pdesmarc/ProjetFilRouge.git
$ cd ProjetFilRouge
```
Once you have cloned the repository and are in it, you need to activate the virtual environment :
```sh
# Activate the virtual environment
$ pipenv shell
```
Then you need to install dependencies (Easy with Pipenv)   :
```sh
# Install dependencies automatically
$ pipenv install
```

## Run the server

### Run the server locally
To run the server locally:
```sh
# Run server (https://localhost:5000)
$ python app.py --debug 1
```

### Run the server in production 
The server is programmed to be run in an Amazon EC2 with FreeBSD 11.0 as OS :
```sh
# Run server (http://YOUR-DNS-PUBLIC-ADRESS:80)
$ python app.py
```
### Endpoints
Here is a list of  the api endpoints : (.../ means where you run your server : ex =  http://localhost:5000)

| Number| HTTP Method | Action | Route
| ------| ------ | ------ | ------ |
| 1 | GET  | Access to the swagger | .../swagger/ |
| 2 | POST  | Submit a file to the api | .../transform |


To test the API, , I strongly recommend to use [Postman]
You can find here a Postman collection with the request to test the *transform* endpoint: [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/7a71c2b7654298355646) 

If you prefer to try the API with the [curl] command, here is a list of curl command example for every mimetype supported with the response associated : 

- *.txt*
```bash
# Curl with .txt file
$ curl -X POST "http://127.0.0.1:5000/transform" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "upfile=@PATH/TO/THE/FILE.txt;type=text/plain"
```
The response will be something as below : 
{ "Data": ["line1",     "line2"  ],   "Metadonnees": { "filename": "filename.txt",  mimetype":"text/plain", "size": "100 o"  }}
- *.csv*
```bash
# Curl with .csv file
$ curl -X POST "http://127.0.0.1:5000/transform" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "upfile=@PATH/TO/THE/FILE.csv;type=text/csv"
```


The response will be something as below:
{ "Data": [    { "column1": "x11",       "column2": "x12"    },     {      "column1": "x21",       "column2": "x22"    }  ],   "Metadonnees": {    "filename": "filename.csv",     "mimetype": "text/csv",     "size": 79 o"  }}


- *.jpg (type=image/jpeg)*, *.jpeg (type=image/jpeg* , *.pdf (type=application/pdf)*, *.png (type=image/png)* 
```bash
# Curl with .jpg, .jpeg , .pdf, .png  file
# The curl below is a for a pdf file, for other mimetype the structure is the same, only the type parameter at the end has to be modified
$ curl -X POST "http://127.0.0.1:5000/transform" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "upfile=@PATH/TO/THE/FILE.pdf ;type=application/pdf"
```
The response will be something as below: 
{ "Data": the data of the file will be encode to base 64. See here the [documentation], "Metadonnees": {    "filename": "filename.pdf",     "mimetype": "application/pdf",     "size": 10000 o"  }} 

[//]: #
   [postman]: <https://www.getpostman.com>
   [pipenv documentation]: <https://pypi.org/project/pipenv/>
   [curl]: <https://curl.haxx.se>
   [documentation]: <https://en.wikipedia.org/wiki/Base64>
