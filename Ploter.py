# -*- coding: utf-8 -*-

import numpy , pandas , controller.DB as DB 
import plotly.graph_objs as go
from tkinter import *
# pip install pillow
from PIL import Image, ImageTk

def Ploter():
    Lat_Long = []
    for i in DB.DATABASE().GET_airport() :
        Lat_Long.append(i[1:4])   
    Data = pandas.DataFrame(numpy.array(Lat_Long),columns=['Code', 'Lat', 'Lng'])
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = Data['Lng'],
        lat = Data['Lat'],
        hoverinfo = 'text',
        text = Data['Code'],
        mode = 'markers',
        marker = dict(
            size = 5,
            color = 'rgb(255, 0, 0)')))
    fig.update_layout(title_text = ' Visualisation des Airoports ',showlegend = True ,
    geo = dict(scope = 'usa', showland = True,landcolor = 'rgb(0, 0, 0)',countrycolor = 'rgb(204, 204, 204)',))
    fig.show()
    fig.write_image("plot.png")
Ploter()
