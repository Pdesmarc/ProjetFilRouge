#encoding : utf-8
import boto3
import argparse
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import base64
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename
from io import BytesIO


#Init app
app = Flask(__name__)
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Swagger Fil Rouge"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

#Init var
metadonne={}
jsonoutput={}
ALLOWED_EXTENSIONS = {'txt', 'csv', 'jpg', 'jpeg' ,'pdf', 'png'} #, 'gif'}

def allowed_file(filename):
    ''' Check if the file respond to our in input criteria
        Args:
            filename (string): The name of the input file
           

        Returns:
            bool: True if the file is allowed to be processed, false if not
        '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_metadata(file):
    '''Retrieve three metadatas for the input file 

        Args:
            file (FileStorage): The input file


        Returns:
            metadate(dictionnary): A dict containing the filename, the mimetype and the size
        '''
    metadata={}
    metadata['mimetype'] = file.mimetype
    metadata['filename'] = file.filename
    metadata['size'] = str(os.fstat(file.stream.fileno()).st_size) + ' o'

    return metadata

def upload_to_s3(datafile, filename):
    '''Upload the file to s3
        Args:
            datafile (FileStorageStream): The input file stream
            filename (string) : The name of the input file


        Returns:
            nothing
        '''
    f =  BytesIO(datafile)
    s3 = boto3.client('s3')
    s3.upload_fileobj(f, 'iaas-projetfilrouge-pdesmarc', filename)

    


@app.route("/transform", methods=['POST'])
def upload_file():
    #Return an error if no file submitted
    if not request.files : 
        return jsonify({'Error ' : 'Please enclose a file'}), 400

    #Return an error if the file is not submitted with a parameter called updfile
    if 'upfile' not in request.files:
        return jsonify({'Error ' : 'In the POST request, the key parameter must be called \'upfile\' '}), 400

    filetodisplay = request.files['upfile']
    if filetodisplay and allowed_file(filetodisplay.filename):
        # Safety first 
        filetodisplay.filename = secure_filename(filetodisplay.filename)

        #get the metadata
        metadonne = get_metadata(filetodisplay)
        jsonoutput['Metadonnees'] = metadonne

        #Upload to s3
        datafile = filetodisplay.read()
        upload_to_s3(datafile, filetodisplay.filename)

        # Retrieve data, specific treatment in function of mimetype file 
        if filetodisplay.mimetype == 'text/plain':  
            #Retrieve each file of the text file                                       
            datafile = datafile.decode('utf-8').splitlines()
            jsonoutput['Data'] = datafile
            

        elif filetodisplay.mimetype == 'text/csv':
            # ',' must be the delimiter of the csv input
            fileString = datafile.decode('utf-8')
            # Retrieve each data with its column associated
            datafile = [{k: v for k, v in row.items()} for row in csv.DictReader(fileString.splitlines(), skipinitialspace=True)]
            jsonoutput['Data']=datafile

        else:
            #For image-like file, we encode the data to Base64. A simply decode64 permit to retrieve the file as submitted           
            data_string = base64.b64encode(datafile)
            jsonoutput['Data']=data_string.decode('utf-8')
            
        return jsonify(jsonoutput)
    #If there is no file submitted even if a parameter called 'upfile' is sent, an error is sent back
    elif not filetodisplay :
        return jsonify({'Error ' : 'Please enclose a file'}), 400
        #If the mimetype is not yet supported, an error is sent back
    else:
        return jsonify({'Error' : 'The mimetype of your file is not yet supported'}), 400



#Run server 
if  __name__=='__main__':

    PARSER = argparse.ArgumentParser(description="Flask API Projet FR")

    # To run the server locally, add this argument ( no matter what is the value associated)
    PARSER.add_argument('--debug', help='Use the API in local with debug mode')
    
    ARGS = PARSER.parse_args()
    if ARGS.debug:
        # Run server in local
        CORS(app, support_credentials=True)
        app.run(debug=True)
    else :
        # Run server not in local
        app.run(host="0.0.0.0", port=80)
