# Graphing 
# import plotly.express as px
# import plotly.graph_objects as go
import io
import base64

def serveChartInMemory(graphingPayload):
    # as opposed to creating JPEG each time, can do one in memory
    # and server per https://stackoverflow.com/questions/25140826/generate-image-embed-in-flask-with-a-data-uri 
    # another example: https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser 
    """
    Take image plot (matplotlib currently), return HTML img element with in-memory image

    Keyword arguments:
    plt -- the graph object

    Sourced from: 
    https://blog.furas.pl/python-flask-how-to-use-bytesio-in-flask-to-display-matplotlib-image-without-saving-in-file-gb.html
   
    graphingPayload = { "graph_type": "bar",
                    "graph_height": 400, 
                    "graph_width": 600, 
                    "x_axis": x, 
                    "y_axis": y,
                    "export_type": "jpeg",
                    "export_location": "report.jpeg",
                    "graph_title": "report",
                    "x_axis_label": "Date",
                    "y_axis_label": "Hours"
                    }
    """
    # Option to run natively  
    # fig = px.bar(   x=graphingPayload['x_axis'], 
    #                 y=graphingPayload['y_axis'], 
    #                 title=graphingPayload['graph_title']
    #             )

    fig = chart(graphingPayload)
    img = io.BytesIO()
    fig.write_image(img, format=graphingPayload["export_type"])
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64,{plot_url}">'