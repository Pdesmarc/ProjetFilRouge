#encoding : utf-8

from flask import Flask, request, jsonify
import os
import csv

#Init app
app = Flask(__name__)

metadonne={}
jsonoutput={}
ALLOWED_EXTENSIONS = {'txt', 'csv'} # 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route("/transform", methods=['POST'])
def upload_file():
    if request.files['data_file']:
        filetodisplay = request.files['data_file']
        if filetodisplay.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            if filetodisplay.mimetype == 'text/plain':
                metadonne['mimetype'] = filetodisplay.mimetype
                metadonne['filename'] = filetodisplay.filename
                datafile = filetodisplay.read().decode('utf-8').splitlines()
                jsonoutput['Metadonnees'] = metadonne
                jsonoutput['Data'] = datafile
                return jsonify(jsonoutput)

            elif filetodisplay.mimetype == 'text/csv':
                # ',' must be the delimiter of the csv input
                metadonne['mimetype'] = filetodisplay.mimetype
                metadonne['filename'] = filetodisplay.filename
                fileString = filetodisplay.read().decode('utf-8')
                datafile = [{k: v for k, v in row.items()} for row in csv.DictReader(fileString.splitlines(), skipinitialspace=True)]
                jsonoutput['Metadonnees'] = metadonne
                jsonoutput['Data']=datafile
                return jsonify(jsonoutput)
        else:
            return 'The mimetype of your file is not yet supported' 
    else:
        return 'Please enclose a file'


#Run server 
if  __name__=='__main__':
    app.run(debug=True)
