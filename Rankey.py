#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


finalNodeData = pd.read_csv('finalNodeData')
finalLinkData = pd.read_csv('finalLinkData')
averages = pd.read_csv('ranks')
test2Artist = {"Test" : "Did Not Make The Charts"}
finalNodeData = finalNodeData.replace(test2Artist)

finalNodeData['Unnamed: 0'] = finalNodeData['Unnamed: 0']+1
finalNodeData['Rank'] = finalNodeData['Unnamed: 0']%51
finalNodeData['Year'] = finalNodeData['Unnamed: 0'].apply(lambda x: x//51 + 2016)

averages['Unnamed: 0'] = averages['Unnamed: 0'] + 2013 

averages = averages.rename(columns={'Unnamed: 0': 'Year', 'MR': 'Rank'})

finalNodeData.merge(averages, on=['Year','Rank'], how='left')


# In[ ]:


from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from PIL import Image
import base64


with open('image.png', "rb") as image_file:
    img_data = base64.b64encode(image_file.read())
    img_data = img_data.decode()
    img_data = "{}{}".format("data:Image/png;base64, ", img_data)


    
app = Dash(__name__)

server = app.server

image_filename = 'concert.svg' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

colors = {
         'background': '#000000',
         'text': '#FFFFFF'
         }

app.layout = html.Div(
    
    style={'backgroundColor': colors['background']},
    children=[
        
        html.Br(),
        
        html.H1(children='Rap Charts 2016-2022', style={'textAlign': 'center','color': colors['text'],'font-size': 40}),
        
        html.H2(children='     Over the past few years, the rap scene has seen a significant increase in the number of women artists. While hip hop \nhas historically been male-dominated, more and more women are breaking through and making their mark on the \ngenre. The data reveals a remarkable trend. From Cardi B to Megan Thee Stallion, women are taking the industry by \nstorm, and the numbers don\'t lie.Whether you\'re a fan of rap or simply interested in the evolution of popular music, this \nvisualization offers a unique insight into a movement that is changing the face of hip hop.',style={"white-space": "pre",'margin-left': '100px','textAlign': 'left','color': colors['text']}),
        
        html.Div([
            
        html.H2(children='Show me:', style={'textAlign': 'left','marginBottom': 0,'margin-left': '100px','color': colors['text'],'font-size': 30}),
        
        dcc.Checklist(
        [
        {
            "label": html.Div(['Men'], style={'color': '#6ca0dc','marginTop': 0, 'font-size': 25}),
            "value": "Men",
        },
        {
            "label": html.Div(['Women'], style={'color': '#fc9cff', 'font-size': 25}),
            "value": "Women",
        },
    
        ], value=['Women', 'Men'], id = 'checklist1', style = {'display':'inline-block','margin-left': '100px'}, labelStyle={"display": "flex", "align-items": "center"}),
        
        dcc.RadioItems(
        [
        {
            "label": html.Div(['All Artists'], style={'color': '#FFFFFF','marginTop': 0, 'font-size': 25}),
            "value": 0,
        },
        {
            "label": html.Div(['Artists Who Charted At least 2 Consecutive Years'], style={'color': '#FFFFFF', 'font-size': 25}),
            "value": 1,
        }
        ],value=1, id = 'checklist2', style = {'display':'inline-block','margin-left': '100px'}, labelStyle={"display": "flex", "align-items": "center"}),
        
        ]),
        html.Br(),
        
        dcc.Graph(id="graph",style={'display': 'flex'}),
        
        html.P("Year"),
        
        dcc.RangeSlider(id='rangeslider', min=2016, max=2022, 
                  marks={
                      2016: {'label': '2016', 'style': {'color': '#FFFFFF', 'font-size': 20}},
                      2017: {'label': '2017', 'style': {'color': '#FFFFFF','font-size': 20}},
                      2018: {'label': '2018', 'style': {'color': '#FFFFFF','font-size': 20}},
                      2019: {'label': '2019', 'style': {'color': '#FFFFFF','font-size': 20}},
                      2020: {'label': '2020', 'style': {'color': '#FFFFFF','font-size': 20}},
                      2021: {'label': '2021', 'style': {'color': '#FFFFFF','font-size': 20}},
                      2022: {'label': '2022', 'style': {'color': '#FFFFFF','font-size': 20}}},
                        
                  value=[2016,2022], step=None, allowCross =False),
    
        
        html.Img(id="tag_id", src=img_data, alt="my image", width="1422", height="200", className = 'align-self-center'),
        
])

layout = go.Layout(
     
        height = 600,
        width = 1420,
    
        margin=go.layout.Margin(
        l=30, #left margin
        r=30, #right margin
        b=10, #bottom margin
        t=10, #top margin
    )
)


@app.callback(
    Output("graph", "figure"), 
    Input("rangeslider", "value"),
    Input("checklist1", "value"),
    Input("checklist2", "value")
    )

def display_sankey(opacity, value, values):
    
    yearS = opacity[0]
    yearE = opacity[1]
    
    if 'Women' in value and 'Men' in value:
        x = 0
    elif 'Women' in value:
        x = 1
    elif 'Men' in value:
        x = 2
        
    
    span = (int(yearE)-int(yearS)+1)
    
    xcords = [['0.0000000001']*51]
    
    for i in range(1, span-1):
    
        xcords.append([str(i/(span-1))]*51)

    xcords = [item for sublist in xcords for item in sublist]+ [0.9999999999]*51
    xcords = sorted([float(x) for x in xcords])
    
    ycords = [0.0000001 + x*(0.99999-0.0000001)/51 for x in range(51)]*span

    
    beginIdx = (yearS-2016)
    endIdx = 7 - (2022-yearE)
    tempN = finalNodeData.iloc[beginIdx*51:endIdx*51]
    tempN = tempN.reset_index(drop=True)
    tempN.at[50, 'NC'] = 'rgba(0,0,0,0)'
    endIdx2 = yearE-2016
    tempLink = finalLinkData[finalLinkData['S'].between(51*beginIdx, 51*(endIdx2)-1, inclusive = 'both')]
    tempLink['S'] = tempLink['S'].apply(lambda x: x-51*(beginIdx))
    tempLink['T'] = tempLink['T'].apply(lambda x: x-51*(beginIdx))
    tempLink = tempLink.reset_index(drop=True)
    
    if values == 1:
        
        tempLink['mod'] = tempLink['T'].apply(lambda x: (int(x)+1)%51)
        tempLink.loc[tempLink['mod'] == 0, 'LC'] = "rgba(0,0,0,0)"
        tempN.loc[tempN['N']=='Did Not Make The Charts', 'NC'] = "rgba(0,0,0,0)"
    
    if x == 0:
        print('great')
    elif x == 1:
        tempN['NC'] = tempN['NC'].apply(lambda c: 'rgba(0,0,0,0)' if c == '#6ca0dc' else c)
        tempLink['LC'] = tempLink['LC'].apply(lambda c: 'rgba(0,0,0,0)' if c == '#6ca0dc' else c)
    elif x == 2:
        tempN['NC'] = tempN['NC'].apply(lambda c: 'rgba(0,0,0,0)' if c == '#fc9cff' else c)
        tempLink['LC'] = tempLink['LC'].apply(lambda c: 'rgba(0,0,0,0)' if c == '#fc9cff' else c)
        
    node = {
           "x": xcords, 
           "y": ycords,  
           "pad" : 30,
           "label" : tempN['N'],
           "color": tempN['NC']
          }

    link = {
           "source" : tempLink['S'],
           "target" : tempLink['T'],
           "value" : [5]*len(tempLink),
           "color" : tempLink['LC'],
           }

    fig = go.Figure(go.Sankey(link=link, node=node),layout=layout)
    fig.update_layout(font=dict(size = 10, color="rgba(0,0,0,0)"), plot_bgcolor='black',paper_bgcolor='black', autosize=False)
    return fig

app.run_server(debug=False)


# In[ ]:





# In[ ]:




