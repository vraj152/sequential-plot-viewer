# Sequential Plot Viewer

* This project is developed as a part of qualifying test given by Professor Tomasz Imieliński, Rutgers University.
* Task: 
  * [Given data](/data/), you need to generate graphs using [Highcharts](https://www.highcharts.com/) and Flask framework.
  * There should be two buttons, using which we can navigate through all the graphs.
  * Host it on cloud.
* Generated two types of graph:
  * [BoxPlot](https://www.highcharts.com/demo/box-plot)
  * [BarGraph with drilldown](https://www.highcharts.com/demo/column-drilldown)

* Code Explaination:
  * Backend:
    * Technologies Used: Python3, Flask, AWS (for hosting web application)
    * Helper Methods:
      * [read_data](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/API/flaskAPIs.py#L4):
        * Argument: Graph type (either boxplot or bargraph)
        * Returns: Returns all plots extracted from entire data after filtering with constraints (AKA slices)
        * Working:
          * It will iterate through entire dataset and filter out data as per the input given
          * Will store all required data for each plot like category, score, support, slices etc.

      * [prepare_response](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/API/flaskAPIs.py#L47):
        * Arguments:
          * curr: Query index of the graph.
          * allplots: All the plots (filtered on current slice)
          * drilled_dic: Initially drilling will be done on static value, but it can be changed to any available value.
          * pref: Desired drill value if any.
        * Returns: Returns response which will be sent to server, and which will help server to render the graph.
        * Working:
          * It will first fetch the corresponding plot using current index (passed as a parameter) and will prepare response.
          * Response will contain following things.
            * index: Which will be displayed on webpage
            * res: Actual Data
            * currcons: Current slice (which will be displayed on webpage)

      * [prepare_box_response](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/API/flaskAPIs.py#L135):
        * Same as above one, but will be used to prepare response for rendering box plots.

    * [API](/entryPoint.py):
      * There are several end points which will be used by Falsk framework and AJAX to render the webpage.

      i) ["/"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L11) -> GET Method:
        * Index page. It will render the template "home.html", which contains form where you can select which graph you want to plot and also you can
        pass dataset for which you want to plot graphs.
        (P.S.: Because I was not very sure with data, I have used the files provided. But it could be changed to make it dynamic.)

      ii) ["/submitdata"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L15) -> POST Method:
        * Whenever form will be submitted, this endpoint will be invoked. It will accept two inputs from the user (form).
          a) plottype: User can select from above mentioned two types. Input type is hidden in form.
          b) file: Dataset file, which is optional as of now.
        * It will fetch the data using [helper method]() by passing plottype as argument. And accordingly template will be renderred.

      iii) ["/render"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L28) -> GET Method:
        * This endpoint will render the first bargraph (passing argument curr=0 denotes, graph with 0 indexed will be returned)
        * It will render template called "render_graph.html", which contains web page where all the bargraphs will be displayed. 

      iv) ["/getplot"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L33) -> GET Method:
        * Whenever next or previous button will be clicked, this endpoint will be invoked. It will accept index of which graph to be displayed. 
        * This will call the same helper method which we call while rendering the first graph, but this time index will not be 0.

      v) ["/updatedrill"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L39) -> GET Method:
        * As stated earlier I have set pre defined categories on which further drilling will be done.
        * Predefined drilling: {"SYMPTOMS": "DRINK", "DRINK": "SYMPTOMS", "MEETINGS": "SYMPTOMS"}
        * In other words: If attribute on which we are plotting graph is Symptoms, then drilling will be done on Drink's data.
        * But let's consider following scenario.
          * _For Example:_ If we have current attribute is Symptoms and slice is set as Drink, then it's not fruitful to drill upon drink.
        * So, to give user freedom of selecting drilling variable, there is dropdown menu where you can select drilling attribute and then to update 
        graph, this endpoint will be invoked.

        * It will get two inputs:
          * plotno: Current plot on which, we are changing drilling variable.
          * drill: User provided drilling attribute.

      vi) ["/renderbox"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L46) -> GET Method:
        * This endpoint will be invoked to plot the boxplot.

      vii) ["/getboxplot"](https://github.com/vraj152/sequential-plot-viewer/blob/9551e3a25a35a9d17814bd11c6ea6e73a9ce0c78/entryPoint.py#L51) -> GET Method:
        * Same as /getplot, this endpoint is used to render the passed indexed plot. (Will be invoked when next/ previous button is clicked.)
      
  * Front end:
    * Technologies Used: HTML, JavaScript, AJAX, HighCharts, CSS
    * [Home page](/templates/home.html):
      * Template borrowed from: https://codepen.io/shubhamc_007/pen/GWvZGN
    * Whenever drill option is changed, AJAX call will be made. Without reloading entire page, we will just refresh the graph data.
    * Whenever we click on next or previous, again AJAX call will be made.
 
* Project Link: https://bit.ly/3i9rGiI (Hosted on AWS.)
* Project Credits: Tomasz Imieliński
* Let me know if you have got question.:raising_hand:
 
    
  
    


