from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import API.flaskAPIs as api

app = Flask(__name__)
CORS(app)

allplots = []
drilled_dic = {"SYMPTOMS": "DRINK", "DRINK": "SYMPTOMS", "MEETINGS": "SYMPTOMS"}

"""
Base URL, whenever localhost:5000 will be hit, this endpoint will be invoked.
Returns template of the home page.
"""

@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")

"""
Whenever form will be submitted, this endpoint will be invoked. It will 
accept two inputs from the user (form). 
    a) plottype: User can select from above mentioned two types. Input type is hidden in form. 
    b) file: Dataset file, which is optional as of now.
    
It will fetch the data using helper method by passing plottype as argument. 
And accordingly template will be renderred.

"""

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
    
"""
This endpoint will render the first bargraph.
Passing argument curr=0 denotes, graph with 0 indexed will be renderred initially
It will render template called "render_graph.html", which contains web page 
where all the bargraphs will be displayed.

"""

@app.route('/render', methods=['GET'])
def render():
    res = api.prepare_response(0, allplots, drilled_dic, "")
    return render_template("render_graph.html", res=res)

"""
Whenever next or previous button will be clicked, this endpoint will be invoked. 
It will accept index of which graph to be displayed.
This will call the same helper method which we call while rendering the first graph, 
but this time index will not be 0.

"""

@app.route('/getplot', methods=['GET'])
def get_plot():
    plotno = request.args.get('plotno')
    res = api.prepare_response(int(plotno), allplots, drilled_dic, "")
    return res

"""
As stated earlier I have set pre defined categories on which further drilling will be done.
Predefined drilling: {"SYMPTOMS": "DRINK", "DRINK": "SYMPTOMS", "MEETINGS": "SYMPTOMS"}

In other words: 
    If attribute on which we are plotting graph is Symptoms, then drilling will be done on Drink's data.

But let's consider following scenario.

For Example: If we have current attribute is Symptoms and slice is set as Drink, then it's not fruitful to drill upon drink.
So, to give user freedom of selecting drilling variable, there is dropdown menu where you can select drilling attribute and then to update graph, this endpoint will be invoked.

It will get two inputs:
    plotno: Current plot on which, we are changing drilling variable.
    drill: User provided drilling attribute.

"""

@app.route('/updatedrill', methods=['GET'])
def update_drill():
    plotno = int(request.args.get('plotno'))
    drill = request.args.get('drill')
    res = api.prepare_response(plotno, allplots, drilled_dic, drill)
    return res

"""
This endpoint will be invoked if we were to render box plot.
Works in similar way to /render.

"""

@app.route('/renderbox', methods=['GET'])
def render_box():
    res = api.prepare_box_response(0, allplots)
    return render_template("boxplot.html", res = res)

"""
This endpoint will be invoked when next/ previous is clicked on box plot
It works in similar way to /getplot.

"""

@app.route('/getboxplot', methods=['GET'])
def get_box_plot():
    plotno = request.args.get('plotno')
    res = api.prepare_box_response(int(plotno), allplots)
    return res

"""
Driver code.

"""

if __name__ == "__main__":
    app.run(host='0.0.0.0')