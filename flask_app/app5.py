import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import string, random, requests
import json
import sys
sys.path.insert(0, '/home/angle/hackathon/captioner')
from amazon.api import AmazonAPI
import requests
# import concurrent.futures
# import urllib.request

access_key = 'AKIAICKBWHEJRIVDWHUA'
secret_key = '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'
associate_tag = 'sagarpatel-20'

import subprocess as sub
import imagecaptioner
app = Flask(__name__, instance_relative_config=True)

upload_folder = '/home/angle/images/'

amazon = AmazonAPI(access_key, secret_key, associate_tag)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # extension = os.path.splitext(file.filename)[1]
        # rand = id_generator()
        # f_name = str(rand) + extension
        # file.save(os.path.join(upload_folder, f_name))
        path = "/home/angle/hackathon/query/img.jpg"
        p = sub.Popen(['python', '/home/angle/tmp/tmp.py'],stdout=sub.PIPE,stderr=sub.PIPE)
        # response_text = os.system("python ")
        output, errors = p.communicate()
        print output
        file.save(os.path.join(path))
        # response_text = get_captions(path)
        # return json.dumps({'filename':f_name})
        return response_text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # extension = os.path.splitext(file.filename)[1]
        # rand = id_generator()
        # f_name = str(rand) + extension
        path = "/home/angle/hackathon/query/img.jpg"
        file.save(os.path.join(path))
        # response_text = get_captions(path)
        # response_text = os.system("python /home/angle/tmp/tmp.py")
        p = sub.Popen(['python', '/home/angle/tmp/tmp.py'],stdout=sub.PIPE,stderr=sub.PIPE)
        # response_text = os.system("python ")
        OUTPUT, errors = p.communicate()
        print OUTPUT
        
        # output = ' '.join(OUTPUT.split()[:3])
        # output = OUTPUT# + ' Men\'s Shirt'
        # products = amazon.search_n(60, Keywords=output, SearchIndex='All')
        # # file.save(os.path.join(upload_folder, f_name))

        # data = []
        # URLS = []

        # for i, product in enumerate(products):
        #     jsn = {}
        #     jsn['asin'] = product.asin
        #     jsn['price'] = product.formatted_price
        #     jsn['img'] = product.large_image_url
        #     URLS.append(jsn['img'])
        #     print(i)
        #     jsn['page'] = product.detail_page_url
        #     data.append(jsn)
        #     try:
        #         with open('../hackathon/ir/{}.jpg'.format(i), 'wb') as f:
        #             f.write(requests.get(jsn['img']).content)
        #         print(jsn['img'])
        #     except:
        #         pass


        return json.dumps({'captions':OUTPUT})

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