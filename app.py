# !pip install azure-core
# !pip install azure-ai-formrecognizer
# !pip install flask-ngrok
# !pip install flask-bootstrap

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import (Flask,g,redirect,render_template,session,url_for)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
# from flask_ngrok import run_with_ngrok

endpoint = "https://nik-formrecognizer-1.cognitiveservices.azure.com/"
key = ""

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

app = Flask(__name__)
# run_with_ngrok(app)
Bootstrap(app)


@app.route('/',methods = ['GET'])
def process_get():
    print("hello")
    return render_template('index.html')


@app.route('/process',methods = ['POST'])
def process():
    try:
        f = request.files['file']
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
        result = poller.result()
        raw_data = result.to_dict()
        table_result = {

        }
        # print(raw_data)
        for data in raw_data['tables']:
            for cell in data['cells']:
                # print(cell)
                if "row_index"+str(cell["row_index"]) in table_result:
                    table_result["row_index"+str(cell["row_index"])].append(cell['content'])
                else:
                    table_result["row_index"+str(cell["row_index"])] = [cell['content']]

        table_data = []
        for data in table_result:
            table_data.append(table_result[data])
        return {"data":table_data,"success":True}
    except Exception as e:
        return {"data":None,"success":False,"message":str(e )}
    
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0',port=5000)