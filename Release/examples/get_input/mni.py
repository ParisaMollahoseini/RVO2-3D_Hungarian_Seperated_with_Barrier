#!/usr/bin/env python
# coding: utf-8

# In[1]:


# http://127.0.0.1:8050


# In[2]:


import pathlib
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()

default_colorscale = [
    [0, "rgb(12,51,131)"],
    [0.25, "rgb(10,136,186)"],
    [0.5, "rgb(242,211,56)"],
    [0.75, "rgb(242,143,56)"],
    [1, "rgb(217,30,30)"],
]


# In[ ]:


def read_mniobj(fp):
    """
    Parses an obj file.
    
    :params file: file name in data folder
    :returns: a tuple
    """
    num_vertices = 0
    matrix_vertices = []
    k = 0
    list_indices, indices = [], []
    
    fp = fp.split()
    
    array = np.array(fp[7:]).reshape((-1,4))
    array = array[:,:-1]
    
    num_vertices = int(fp[6])
    matrix_vertices = np.zeros([num_vertices, 3])
    
    for i in range(len(array)):
        
        if i < num_vertices:
            matrix_vertices[i] = list(map(float, array[i]))
        elif i >= num_vertices:
            list_indices.append(list(map(int, array[i])))
    
#     for i in range(len(indices)-2):
#         list_indices.append(list(map(int,[indices[i],indices[i+1],indices[i+2]])))
    
    #print(matrix_vertices,'--------------------',list_indices)
    
    if len(list_indices) > 0 :
        faces = np.array(list_indices)
        return matrix_vertices, faces-1
    else:
        return matrix_vertices, list_indices


# In[ ]:


def plotly_triangular_mesh(
    vertices,
    faces,
    intensities=None,
    colorscale="Viridis",
    flatshading=True,
    showscale=False,
    plot_edges=False,
):

    x, y, z = vertices.T
    if len(faces) > 0:
        I, J, K = faces.T
    else:
        I, J, K = [], [], []

    #print('x: ',x,'\n','I: ',I)
    if intensities is None:
        intensities = z

    mesh = {
        "type": "mesh3d",
        "x": x,
        "y": z,
        "z": y,
        "colorscale": colorscale,
        "intensity": intensities,
        #"flatshading": flatshading,
        "i": I,
        "j": K,
        "k": J,
        "name": "",
        "showscale": showscale,
#         "lighting": {
#             "ambient": 0.18,
#             "diffuse": 1,
#             "fresnel": 0.1,
#             "specular": 1,
#             "roughness": 0.1,
#             "facenormalsepsilon": 1e-6,
#             "vertexnormalsepsilon": 1e-12,
#         },
         #"lightposition": {"x": -100, "y": 200, "z": 0},
    }
    
    #line --- fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
    #print(mesh)
    line_data = []
    
    for i in range(len(J)):
        #print(I[i],J[i],K[i])
        if J[i]==K[i]:
            line = {}
            line["x"]= [x[I[i]],x[J[i]]]
            line["z"]= [y[I[i]],y[J[i]]]
            line["y"]= [z[I[i]],z[J[i]]]
            line["type"] = 'scatter3d'
            line["mode"] = 'lines'
            line["colorscale"]= colorscale
            line_data.append(line)
            #line_data.append(px.line_3d(z=[y[I[i]],y[J[i]]], x=[x[I[i]],x[J[i]]], y=[z[I[i]],z[J[i]]]))
    
    #line_data = go.Scatter(x=i_line, y=j_line)
    #line_data = px.line_3d(z=y, x=i_line, y=j_line)
    #print('line data:\n',line_data[0])
    #line
    
    if showscale:
        mesh["colorbar"] = {"thickness": 20, "ticklen": 4, "len": 0.75}

    #print('mesh:',mesh)
    if plot_edges is False:
        if np.all(mesh["j"]==mesh["k"]):
            print('line--------------')
            return line_data
        else:
            ret = [mesh]
            ret.extend(line_data)
            print('ret is : \n',ret)
            return ret

    lines = create_plot_edges_lines(vertices, faces)
    return [mesh, lines]



# In[ ]:


def create_plot_edges_lines(vertices, faces):
    tri_vertices = vertices[faces]
    Xe = []
    Ye = []
    Ze = []
    for T in tri_vertices:
        Xe += [T[k % 3][0] for k in range(4)] + [None]
        Ye += [T[k % 3][1] for k in range(4)] + [None]
        Ze += [T[k % 3][2] for k in range(4)] + [None]

    # define the lines to be plotted
    lines = {
        "type": "scatter3d",
        "x": Xe,
        "y": Ye,
        "z": Ze,
        "mode": "lines",
        "name": "",
        "line": {"color": "rgb(70,70,70)", "width": 1},
    }
    return lines



# In[ ]:


import sys
def obj_to_mesh(in_file):
    
    num_vertices = 0
    matrix_vertices = []
    tr_final = []
    k = 0
    list_indices, indices = [], []    


    filedata = in_file.split('\n')
    #print('filedata: ',filedata)
    out_data = '';


    # Vertices
    matrix_vertices = [l.split(' ') for l in filedata if l[0:2] == 'v ']
    matrix_vertices = [(float(x[1]), float(x[2]), float(x[3])) for x in matrix_vertices]

    #print("Converting %i Vertices..." % len(matrix_vertices))
    #print(matrix_vertices)
    num_vertices = len(matrix_vertices)

    triangles = [l.split(' ')[1:] for l in filedata if (l[0:2] == 'f ' or l[0:2]=='l ')]
    #print(triangles)
    tr_final = []
    for t in triangles:
        if len(t)==2:
            tr_final.append((int(t[0].split('/')[0]), int(t[1].split('/')[0]), int(t[1].split('/')[0])))
        elif len(t)==3:
            tr_final.append((int(t[0].split('/')[0]), int(t[1].split('/')[0]), int(t[2].split('/')[0])))
        elif len(t)>3:
            for i in range(1,len(t)-1):
                tr_final.append((int(t[0].split('/')[0]), int(t[i].split('/')[0]), int(t[i+1].split('/')[0])))


    #triangles = [(int(t[1].split('/')[0]), int(t[2].split('/')[0]), int(t[3].split('/')[0])) for t in triangles]

    #print("Converting %i Triangles…" % len(tr_final))
    tr_final = np.array(tr_final).reshape((-1,3))
    #print('tr_final: ',tr_final)
    
    #print(matrix_vertices,'----------------tr_final----',tr_final)
    
    if len(tr_final) > 0 :
        faces = np.array(tr_final)
        return np.array(matrix_vertices), faces-1
    else:
        return np.array(matrix_vertices), tr_final    
    
    


# In[ ]:


def create_mesh_data(option,filename):

    data = []
    if filename.split('.')[-1] == 'mesh':
        vertices, faces = read_mniobj(option)
    elif filename.split('.')[-1] == 'obj':
        vertices, faces = obj_to_mesh(option)
    
    #print('filname: ',filename)
    
    data = plotly_triangular_mesh(
        vertices, faces, None, colorscale=default_colorscale
    )

    #data[0]["name"] = filename
    return data

#     if option == "mouse":
#         vertices, faces = read_mniobj("mouse_brain_outline.obj")
#         outer_mesh = plotly_triangular_mesh(vertices, faces)[0]
#         outer_mesh["opacity"] = 0.5
#         outer_mesh["colorscale"] = "Greys"
#         data.append(outer_mesh)

#     if option == "text":
#         vertices, faces = read_mniobj("text.mesh")
# #         intensities = np.loadtxt(DATA_PATH.joinpath("text.txt"))
#     elif option == "human_atlas":
#         vertices, faces = read_mniobj("square.mesh")
# #        intensities = np.loadtxt(DATA_PATH.joinpath("square.txt"))
#     elif option == "mouse":
#         vertices, faces = read_mniobj("circle.mesh")
# #         intensities = np.loadtxt(DATA_PATH.joinpath("mouse_map.txt"))
#     else:
#         raise ValueError

