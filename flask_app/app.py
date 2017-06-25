import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import string, random, requests
import json

app = Flask(__name__, instance_relative_config=True)

upload_folder = '/home/angle/images/'

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
#        extension = os.path.splitext(file.filename)[1]
#        rand = id_generator()
#        f_name = str(rand) + extension
	path = '/home/angle/hackathon/query/img.jpg'
        file.save(path)
#        return json.dumps({'filename':f_name})
	return path

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        rand = id_generator()
        f_name = str(rand) + extension
        file.save(os.path.join(upload_folder, f_name))
        return json.dumps({'filename':f_name})

    	# file = request.files['file']
    	# filename = secure_filename(file.filename)
    	# fileextension = filename.rsplit('.',1)[1]
     #    Randomfilename = id_generator()
     #    filename = Randomfilename + '.' + fileextension
     #    try:
     #        blob_service.create_blob_from_stream(container, filename, file)
     #    except Exception:
     #        print 'Exception=' + Exception 
     #        pass
     #    ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
     #    return '''
	    # <!doctype html>
	    # <title>File Link</title>
	    # <h1>Uploaded File Link</h1>
	    # <p>''' + ref + '''</p>
	    # <img src="'''+ ref +'''">
	    # '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run(port=8000,debug=True)
