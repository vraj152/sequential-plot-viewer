import pandas as pd
import json

main_data = pd.read_csv(r"C:/Users/Dell/sequentialPlotViewer/data/allergyBoundelss.csv")
data_point = pd.read_csv(r"C:/Users/Dell/sequentialPlotViewer/data/allergy_test.csv")

selected_graph = "bargraph"

bar_data = main_data[main_data.plottype == selected_graph]
cnt = 0

for index, data in bar_data.iterrows():
    cnt += 1
    constraints = json.loads(data.slice)
    fdata = data_point
    
    for i, j in constraints.items():
        fdata = fdata[fdata[i] == j]
    
    