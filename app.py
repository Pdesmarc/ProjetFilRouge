from flask import Flask, request, jsonify
import os

#Init app
app = Flask(__name__)

metadonne={}
jsonoutput={}

@app.route("/transform", methods=['POST'])
def upload_file():
    if request.files['data_file']:
        filetodisplay = request.files['data_file']
        if filetodisplay.mimetype == 'text/plain':
            metadonne['mimetype'] = filetodisplay.mimetype
            metadonne['filename'] = filetodisplay.filename
            datafile = filetodisplay.read().decode('utf-8').split("\n")
            jsonoutput['Metadonnees'] = metadonne
            jsonoutput['Data'] = datafile
            return jsonify(jsonoutput)
        else:
            return 'The mimetype of your file is not yet supported'
    else:
        return 'Please enclose a file (only POST Request accepted for the moment)'


#Run server 
if  __name__=='__main__':
    app.run(debug=True)
