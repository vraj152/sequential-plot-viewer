import pandas as pd
import json

def read_data():
    main_data = pd.read_csv(r"./data/allergyBoundelss.csv")
    data_point = pd.read_csv(r"./data/allergy_test.csv")
    
    selected_graph = "bargraph"

    bar_data = main_data[main_data.plottype == selected_graph]
    cnt = 0
    
    allplots = {}
    
    for index, data in bar_data.iterrows():
        first_attr = data.first_attr
        xcord = data.data
        constraints = json.loads(data.slice)
        fdata = data_point
        temp = ""
        
        for i, j in constraints.items():
            temp += i + ", "
            fdata = fdata[fdata[i] == j]
        
        allplots[cnt] = {"first_attr": first_attr, "data": fdata, "xcord" : xcord , "cons":temp}
        cnt += 1
        
    return allplots

def prepare_response(curr, allplots, drilled_dic, pref):
    curr_plot = allplots[curr]
    
    category = curr_plot["first_attr"]
    curr_data = curr_plot["data"]
    const = curr_plot["cons"]
    xcord = json.loads(curr_plot["xcord"])
    
    curr_xcord = {}
    
    for i in xcord[0]:
        curr_xcord[i[0]] = i[1]
    
    if(pref==""):
        drilled_cat = drilled_dic[category]
    else:
        drilled_cat = pref
        
    count_dic = {}
    total_dic = {}
    
    for index, data in curr_data.iterrows():
        cat = data[category]
        drill_val = data[drilled_cat]
        
        if(cat in total_dic):
            total_dic[cat] += 1
        else:
            total_dic[cat] = 1
            
        if(cat in count_dic):
            if(drill_val in count_dic[cat]):
                count_dic[cat][drill_val] += 1
            else:
                count_dic[cat][drill_val] = 1
        else:
            count_dic[cat] = {drill_val: 1}
        
    
    first_data = []
    second_data = []
        
    for i in curr_xcord:
        temp = {}
        temp['name'] = i
        temp['y'] = curr_xcord[i]
        temp['drilldown'] = i
        
        first_data.append(temp)
        
    for i in curr_xcord:
        temp = {}
        temp['name'] = i
        temp['id'] = i 
        
        temp_data = []
        
        if(i in count_dic):
            for j in count_dic[i]:
                ls = []
                ls.append(j)
                ls.append((count_dic[i][j] / total_dic[i]) * 100)
            
                temp_data.append(ls)
            
        temp['data'] = temp_data
        second_data.append(temp)

    res = {}
    res['chart'] = {'type': 'column'}
    res['title'] = {'text': category[0]+category[1:].lower() +  ' Frequence Distribution'} 
    res['subtitle'] = {'text': 'Click on the any column to view further drilldown.'}
    res['accessibility'] = {'announceNewData': {'enabled': True}}
    res['xAxis'] = {'type':'category'}
    res['yAxis'] = {'title': {'text' : 'Frequency Distribution of each value of' + category[0]+category[1:].lower() + 'attribute'}}
    res['legend'] = {'enabled': False}
    res['plotOptions'] = {'series' : {'borderWidth' :0, 'dataLabels': {'enabled':True, 'format': '{point.y:.1f}%'}}}
    res['series'] = [{'name':category, 'colorByPoint': True, 'data': first_data}]
    res['drilldown'] = {'series': second_data}

    final_res = {"index":curr, "res":res, "currcons": const}
    final_res = json.dumps(final_res)
    return final_res