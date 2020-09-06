from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import API.flaskAPIs as api

app = Flask(__name__)
CORS(app)

allplots = api.read_data()
drilled_dic = {"SYMPTOMS": "DRINK", "DRINK": "SYMPTOMS", "MEETINGS": "SYMPTOMS"}

@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")

@app.route('/submitdata', methods=['POST'])
def upload_file():
    allowed_files = ['application/vnd.ms-excel','text/plain','text/csv','text/tsv']
    uploaded_file = request.files['file']
    
    if(uploaded_file.filename == '' or uploaded_file.content_type not in allowed_files):
        flash("File type not allowed, please upload valid file!")
        return redirect(url_for("index"))
    
    return redirect(url_for("render"))

@app.route('/render', methods=['GET'])
def render():
    res = api.prepare_response(0, allplots, drilled_dic, "")
    return render_template("render_graph.html", res=res)

@app.route('/getplot', methods=['GET'])
def get_plot():
    plotno = request.args.get('plotno')
    res = api.prepare_response(int(plotno), allplots, drilled_dic, "")
    return res

@app.route('/updatedrill', methods=['GET'])
def update_drill():
    plotno = int(request.args.get('plotno'))
    drill = request.args.get('drill')
    res = api.prepare_response(plotno, allplots, drilled_dic, drill)
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0')