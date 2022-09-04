#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import os
import signal
import subprocess
from pathlib import Path
import json
import dash
from dash import dcc
import dash_html_components as html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from mni import create_mesh_data, default_colorscale
import dash_reusable_components as drc
import utils
import base64
import webbrowser



app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "Brain Surface Viewer"

server = app.server

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-brain-viewer",
)

default_colorscale_index = [ea[1] for ea in default_colorscale]

param_list = ("timeStep","neighborDist","maxNeighbors","timeHorizon","radius","maxSpeed","velocity_x",
              "velocity_y","velocity_z","fileName")
list_param =[]
for _ in param_list:
    if _ != "fileName":
             list_param.append(
                 html.Div(
                            [
                        html.Label(
                            "{}".format(_),
                            className="label__option"
                            ,style={
                                "width": "100px"
                            }
                                  ),
                        dcc.Input(
                            id="{}".format(_), type="number", placeholder=0.0,className="input__option",
                            style={
                                    "background-color": "#292929",
                                    "border": "1px solid #C4CDD5",
                                    "border-radius": "0.5rem",
                                    "color": "white",
                            }
                        )
                            ]
                        )    
                              )
    else:
             list_param.append(
         html.Div(
                    [
                html.Label(
                    "{}".format(_),
                    className="label__option"
                    ,style={
                        "width": "100px"
                    }
                          ),
                dcc.Input(
                    id="{}".format(_), type="text", placeholder=0.0,className="input__option",
                    style={
                            "background-color": "#292929",
                            "border": "1px solid #C4CDD5",
                            "border-radius": "0.5rem",
                            "color": "white",
                    }
                )
                    ]
                )    
                      )



axis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}
xaxis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
    "autorange": "reversed"
}



plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    "plot_bgcolor": "#141414",
    "paper_bgcolor": "#141414",
    "scene": {
        "xaxis": xaxis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectratio": {"x": 1, "y": 1, "z": 1},
        "camera": {"eye": {"x": 0, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

#new
global len_fig


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=app.get_asset_url("dash-logo.png")
                                        ),
                                        html.H4("MRI Reconstruction"),
                                    ],
                                    className="header__title",
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            "Click on the brain to add an annotation. Drag the black corners of the graph to rotate."
                                        )
                                    ],
                                    className="header__info pb-20",
                                ),
                                html.Div(
                                    [
                                        html.A(
                                            "View on GitHub",
                                            href=GITHUB_LINK,
                                            target="_blank",
                                        )
                                    ],
                                    className="header__button",
                                ),
                            ],
                            className="header pb-20",
                        ),
                        html.Div(
                            [
                              dcc.Graph(
                                    id="brain-graph",                                   
                                    figure={
                                        "data":[],
                                        "layout": plot_layout,
                                    },
                                    config={"editable": True, "scrollZoom": False},
                                  
                                )                                
                                                               
                            ],
                            className="graph__container",
                        ),
                    ],
                    className="container",
                )
            ],
            className="two-thirds column app__left__section",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    "Click colorscale to change", className="subheader"
                                ),
                                dcs.DashColorscales(
                                    id="colorscale-picker",
                                    colorscale=default_colorscale_index,
                                ),
                            ]
                        )
                    ],
                    className="colorscale pb-20",
                ),
                html.Div(
                    [
                        html.P("Select Image", className="subheader"),
                            drc.Card(
                                [
                                    dcc.Upload(
                                        id="upload-image",
                                        children=[
                                            "Drag and Drop or ",
                                            html.A(children="Select a file"),
                                        ],
                                        # No CSS alternative here
                                        style={
                                            "color": "darkgray",
                                            "width": "100%",
                                            "height": "50px",
                                            "lineHeight": "50px",
                                            "borderWidth": "1px",
                                            "borderStyle": "dashed",
                                            "borderRadius": "5px",
                                            "borderColor": "darkgray",
                                            "textAlign": "center",
                                            "padding": "2rem 0",
                                        },
#                                         accept="image/*",
                                    ),
                                ]
                    ),
                    ],
                    className="pb-20",
                ),
                html.Div([
                        html.P("Select option", className="subheader"),
                        dcc.RadioItems(
                            options=[
                                    {"label": " Start", "value": "start"},                                
                                    {"label": " Goal", "value": "goal"},
                            ],
                            value="start",
                            id="radio-options",
                            labelClassName="label__option",
                            inputClassName="radio_input__option",
                        )
                ]
                    ,className="pb-20",
                ),
                html.Div([
                        dcc.Checklist(
                            ['Show simluator'],
                            id = "showsim",
                            inline=True,
                            labelClassName="label__option",
                        )
                ]
                    ,className="pb-20",
                ),                
                html.Div(
                    [
                        html.Span("Parameters", className="subheader"),
                        html.Span("  |  "),
                        html.Span(
                            "Write down the requested parameters.", className="small-text",                            
                        ),
                        html.Div(list_param)

                    ]
                    ,className="pb-20",              
                ),
                html.Div(
                    [
                        html.Span("Click data", className="subheader"),
                        html.Span("  |  "),
                        html.Span(
                            "Click on points in the graph.", className="small-text"
                        ),
                        dcc.Loading(
                            html.Pre(id="click-data", className="info__container"),
                            type="dot",
                        ),
                    ],
                    className="pb-20",
                ),
                html.Div([
                    
                    html.Button(
                            "Save to file", 
                            id="button-save",
                            style={
                                    "color": "white",
                                    "borderWidth": "1px",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin-top": "12px",
                                    "margin-left": "30%"          
                            }  
                        ,className="header__button",
                        ),
                    html.Button(
                            "Send to algorithm", 
                            id="send-algo",
                            style={
                                    "color": "white",
                                    "borderWidth": "1px",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin-top": "12px",
                                    "margin-left": "25%"          
                            }  
                        ,className="header__button",
                        )                    
                ]
                    ,className="pb-20",
                ) ,               
            ],
            className="one-third column app__right__section",
        ),
        dcc.Store(id="annotation_storage")
        ,
        html.Div(id='hidden-div', style={'display':'none'}),
        html.Div(id='hidden-div-2', style={'display':'none'}),
    ]
)


def add_marker(x, y, z):
    """ Create a plotly marker dict. """

    return {
        "x": [x],
        "y": [y],
        "z": [z],
        "mode": "markers",
        "marker": {"size": 15, "line": {"width": 3}},
        "name": "Marker",
        "type": "scatter3d",
    }


def add_annotation(x, y, z):
    """ Create plotly annotation dict. """

    return {
        "x": x,
        "y": y,
        "z": z
    }


def marker_in_points(points, marker):
    """
    Checks if the marker is in the list of points.
    
    :params points: a list of dict that contains x, y, z
    :params marker: a dict that contains x, y, z
    :returns: index of the matching marker in list
    """
    global len_fig

    for index, point in enumerate(points):
        if (index >= (len_fig) 
            and point["x"] == marker["x"]
            and point["y"] == marker["y"]
            and point["z"] == marker["z"]
        ):
            return index
    return None


######################## Update Layout ##########################
@app.callback(
    Output("hidden-div", "children"),
        [
        
        Input("brain-graph", "relayoutData"),
    ]
)
def save_layout_data(layout_data):
    global layout
    
    if layout_data:
        for key in layout_data.keys():
            if bool(re.match(r"scene.[a-z]+", key)):
                layout[key[6:]] = (layout_data[key])
    else:
        layout = {}
    
    print('----------------------------------------------------')
    print('layout data now:\n',layout_data)
    return json.dumps({"saved":"layout"}, indent=4)      
#################################################################
######################## Send Data To Algorithm #################
@app.callback(
    Output("hidden-div-2", "children"),
        [
        Input("send-algo", "n_clicks"),
    ]
)
def save_layout_data(click):
    global startPoints, goalPoints, savedFile, RADIUS, showSim
    
    cur_path = Path(os.getcwd())
    cur_parent = cur_path.parent
    
    command = './Sphere {}.json > {}.txt'.format(savedFile,savedFile)
    process = subprocess.Popen((command), shell=True ,stdout=subprocess.PIPE, cwd=str(cur_parent))
    
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    if showSim:      
        command = 'python3 run_offline_vpython.py -i {}.txt -r {}'.format(savedFile,RADIUS)
        process = subprocess.Popen((command), shell=True ,stdout=subprocess.PIPE, cwd=str(cur_parent))
        
        while True:
            if process.poll() is not None:
                os.kill(os.getpid(),signal.SIGTERM)
                break
#         while True:
#             output = process.stdout.readline()
#             if output == b'' and process.poll() is not None:
#                 break
#             if output:
#                 print(output.strip())
    
    
    return json.dumps({"sent":"annotatio"}, indent=4)    
#################################################################
################### Update figure and clicked data ##############
global filename, clicked, goalPoints, startPoints, layout, RADIUS

RADIUS = 1.5
layout = {}
startPoints, goalPoints = [], []
clicked = 0
filename = ''

@app.callback(
    Output("brain-graph", "figure"),
        [
        State("brain-graph", "figure"),
        State("annotation_storage", "data"),
        State("upload-image", "filename"),
        State("brain-graph", "relayoutData"),
    ],
    [
        Input("brain-graph", "clickData"),
        Input("upload-image", "contents"),
        Input("colorscale-picker", "colorscale"),
    ],

)
def brain_graph_handler(figure, current_anno,new_filename, layout_data, click_data, content,colorscale):
    """ Listener on colorscale, option picker, and graph on click to update the graph. """
    global filename, len_fig, layout
    
    if new_filename and new_filename != filename:
        
        filename = new_filename
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        final_file = decoded.decode("ascii")

        figure["data"] = create_mesh_data(final_file,new_filename)
        figure["layout"] = plot_layout
        cs = [[i / (len(colorscale) - 1), rgb] for i, rgb in enumerate(colorscale)]
        len_fig = len(figure["data"])

        figure["data"][0]["colorscale"] = cs        


    elif filename == new_filename:
        # modify graph markers
        if click_data is not None and "points" in click_data:

            y_value = click_data["points"][0]["y"]
            x_value = click_data["points"][0]["x"]
            z_value = click_data["points"][0]["z"]

            marker = add_marker(x_value, y_value, z_value)
            point_index = marker_in_points(figure["data"], marker)

            # delete graph markers
            if len(figure["data"]) > len_fig and point_index is not None:

                #print('removed: ',point_index)
                figure["data"].pop(point_index)
                anno_index_offset = len_fig
                try:
                    figure["layout"]["scene"]["annotations"].pop(
                        point_index - anno_index_offset
                    )
                except Exception as error:
                    print(error)
                    pass

            # append graph markers
            else:

                # iterate through the store annotations and save it into figure data
                if current_anno is not None:
                    for index, annotations in enumerate(
                        figure["layout"]["scene"]["annotations"]
                    ):
                        for key in current_anno.keys():
                            if str(index) in key:
                                figure["layout"]["scene"]["annotations"][index][
                                    "text"
                                ] = current_anno[key]

                figure["data"].append(marker)
                figure["layout"]["scene"]["annotations"].append(
                    add_annotation(x_value, y_value, z_value)
                )

            cs = [[i / (len(colorscale) - 1), rgb] for i, rgb in enumerate(colorscale)]

            figure["data"][0]["colorscale"] = cs

    if layout != {}:
        for key in layout.keys():
            figure["layout"]['scene'][key] = layout[key]
    print('----------------------------------------------------')
    print("figure layout is now:\n",figure["layout"]['scene'])
    return figure
#################################################################
########################### Save Annotation Data ################
global savedFile, showSim
savedFile = filename

showSim = False

input_list = []
for i in param_list:
    input_list.append(
        Input(i, "value")
    )

@app.callback(
    Output("click-data", "children"),
        [
        State("brain-graph", "figure"),
    ],
    [
        Input("button-save", "n_clicks"),
        Input("radio-options","value"),
        Input("showsim","value"),
        input_list,   
    ],

)
def save_annotations(figure, click_button, target_radio, is_show, *values):
    global filename, clicked, goalPoints, startPoints, len_fig, savedFile, showSim

    new_saved_file = savedFile + '.json'
    
    if is_show and is_show[0] == "Show simluator":
        showSim = True
    else:
        showSim = False
        
    if click_button and click_button > clicked:
        points = []
        dictionary = {}        
        dictionary['startPoints'] = []
        dictionary['goalPoints'] = []
        
        #get annotation points
        for annot in figure["layout"]["scene"]["annotations"]:
            points.append([annot["x"],annot["y"],annot["z"]])        

        #put in dict            
        if target_radio == "start":
            dictionary['startPoints'] = points
            dictionary['goalPoints'] = goalPoints
            startPoints = points
        else:
            dictionary['goalPoints'] = points  
            dictionary['startPoints'] = startPoints
            goalPoints = points
            
        #put other params in dict
        counter = 0
        for i in values:
            for val in i:
                if counter < len(param_list)-1:
                    if counter >= 6:
                        dictionary[param_list[counter]] = val if val else  0
                    else:
                        dictionary[param_list[counter]] = val if val else -1 
                        
                    if counter == 4:
                        RADIUS = val if val else 1.5
                        
                    counter += 1
                else:
                    new_saved_file = val + '.json'
                    savedFile = val


        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)

        # Writing to sample.json
        cur_path = Path(os.getcwd())
        cur_parent = cur_path.parent   
        
        with open(os.path.join(cur_parent,new_saved_file), "w") as outfile:
            outfile.write(json_object)   
        
        clicked = click_button
        
        return json.dumps({"saved file":new_saved_file}, indent=4)        
        
#################################################################
        


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:8050/', new=2)
    app.run_server(debug=True)
    
    

