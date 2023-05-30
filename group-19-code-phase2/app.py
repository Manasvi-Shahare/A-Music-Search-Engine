from flask import Flask, render_template, request, url_for, send_from_directory
#from flask import Flask,render_template,request
#from flask_ngrok import run_with_ngrok
import json
#from PIL import Image
import base64
import io
from bert import bert_search
from pylucene import pylucene_search

# initialize the Flask app
app = Flask(__name__)

# define a route for the home page
@app.route('/')
def msg():
    return render_template('index.html')


# @app.route('/static/<path:path>')
# def serve_static(path):
#     return send_from_directory('static', path)

# define a route for the BERT search page
@app.route("/bert", methods=['POST','GET'])
def bert():
    search_term = request.form["input"]
    res,res1= bert_search(search_term)
    #print(res)
    #print(res1)
    # pass the search results to the bert.html template
    return render_template('bert.html',res=res,res1=res1)

# define a route for the PyLucene search page
@app.route("/pylucene", methods=['POST','GET'])
def pylucene():
    search_term = request.form["input"]
    res,res1= pylucene_search(search_term)
    #print(res)
    #print(res1)
    # pass the search results to the pylucene.html template
    return render_template('pylucene.html',res=res,res1=res1)

# main driver function
if __name__ == '__main__':
    # run the app on a specific host and port
	app.run(host='class-059.cs.ucr.edu', port=8888)