import json
import plotly.express as px
from os.path import exists
import time


def chart():

    start_time = time.time()

    while not exists('chart.json'):
        print('Waiting for file...')
        print(f'{round(time.time() - start_time)} seconds since process began.\n')
        time.sleep(3)

    with open('chart.json', 'r') as f:
        data = json.load(f)
        print('File Opened Successfully!')

    # Optionals
    if 'group' in  data:
        color = data['group']
    else:
        color = None

    if 'graph_title' in  data:
        graph_title = data['graph_title']
    else:
        graph_title = None

    if 'x_axis_label' in  data:
        x_axis_label = data['x_axis_label']
    else:
        x_axis_label = None

    if 'y_axis_label' in  data:
        y_axis_label = data['y_axis_label']
    else:
        y_axis_label = None

    if 'group_label' in  data:
        group_label = data['group_label']
    else:
        group_label = None

    if 'export_location' in data:
        export_location = data['export_location']
    else:
        export_location = ""

    # Line Chart
    if data['graph_type'] == 'line':
        fig = px.line(
            height=data['graph_height']
            ,width=data['graph_width']
            ,x= data['x_axis']
            ,y= data['y_axis']
            ,template= 'simple_white'
            ,color=color
            ,title= graph_title
            ,labels={'x': x_axis_label, 'y':y_axis_label, 'color':group_label}
            )
        fig.write_image(export_location + '.' + data['export_type'])
        print('Line graph exported successfully!\n')
    
    # Bar Chart
    if data['graph_type'] == 'bar':
        fig = px.bar(
            barmode='group'
            ,height=data['graph_height']
            ,width=data['graph_width']
            ,x= data['x_axis']
            ,y= data['y_axis']
            ,template= 'simple_white'
            ,color=color
            ,title= graph_title
            ,labels={'x': x_axis_label, 'y':y_axis_label, 'color':group_label}
            )
        fig.write_image(export_location + '.' + data['export_type'])
        print('Bar graph exported successfully!\n')

    # Scatter Chart
    if data['graph_type'] == 'scatter':
        fig = px.scatter(
            height=data['graph_height']
            ,width=data['graph_width']
            ,x= data['x_axis']
            ,y= data['y_axis']
            ,template= 'simple_white'
            ,color=color
            ,title= graph_title
            ,labels={'x': x_axis_label, 'y':y_axis_label, 'color':group_label}
            )
        fig.write_image(export_location + '.' + data['export_type'])
        print('Scatter graph exported successfully!\n')

chart()