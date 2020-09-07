from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import API.flaskAPIs as api

app = Flask(__name__)
CORS(app)

allplots = []
drilled_dic = {"SYMPTOMS": "DRINK", "DRINK": "SYMPTOMS", "MEETINGS": "SYMPTOMS"}

@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")

@app.route('/submitdata', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    plottype = request.form.get('plottype')
    
    global allplots
    allplots = api.read_data(plottype)
    
    if(plottype=='bargraph'):
         return redirect(url_for("render"))
    elif(plottype=='boxplot'):
        return redirect(url_for("render_box"))
    
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

@app.route('/renderbox', methods=['GET'])
def render_box():
    res = api.prepare_box_response(0, allplots)
    return render_template("boxplot.html", res = res)

@app.route('/getboxplot', methods=['GET'])
def get_box_plot():
    plotno = request.args.get('plotno')
    res = api.prepare_box_response(int(plotno), allplots)
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0')