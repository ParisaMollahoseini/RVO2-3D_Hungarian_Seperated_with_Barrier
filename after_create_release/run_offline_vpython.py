#!/usr/bin/env python
# coding: utf-8

# In[26]:


from vpython import *
import argparse
from random import randint


# In[27]:


from functools import reduce
from timeit import repeat
from tkinter import EXCEPTION
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
from ast import literal_eval as make_tuple
from math import sqrt
import argparse
import numpy as np
from random import choice


# In[28]:


scene = canvas(width=1000, height=500)


# In[29]:


global running, obst_indx
obst_indx = []
running = True

def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"
    
button(text="Pause", pos=scene.title_anchor, bind=Run)
scene.append_to_title('             ')
time_text = wtext(text='travel time = {}'.format(0),pos=scene.title_anchor,)


# In[31]:


def setspeed(s):
    rate_text.text = '{:1.2f}'.format(s.value)

scene.append_to_caption(' Time between each step:   ')    
rate_slider = slider(step=0.01,min=0.01, max=0.5, value=0.25, length=220, bind=setspeed, right=15,top=20,pos=scene.caption_anchor)

rate_text = wtext(text='{:1.2f}'.format(rate_slider.value))


# In[6]:


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# In[7]:


def read_log(file_name:str):
    f = open(file_name , 'r')
    f_lines = f.read().split('\n')
    f_lines.pop()
    f.close()
    return f_lines


# In[8]:


def convert_str2tup(inp:str):
    list_of_tuple = [make_tuple(i) for i in inp.split()[1:]]
    return list_of_tuple

def distance_between(first, second):
      return sqrt((first[0]-second[0]) ** 2 + (first[1]-second[1]) ** 2 + (first[2]-second[2]) ** 2)

def check_collision(all_positions, radius):
    global obst_indx
    collisions = []
    for i in range(len(all_positions)):
        for j in range(i, len(all_positions)):
            if (i in obst_indx) and (j in obst_indx):
                continue
            if i == j:
                continue
            distance = distance_between(all_positions[i], all_positions[j])
            if distance <= 2*radius:
                collisions.append((all_positions[i], all_positions[j]))
    return collisions


# In[9]:


def build_agents(num,MAIN_LIST,Radius):
    

    color_list = [
                (205/255, 7/255, 30/255),
                (255/255, 166/255, 0),
                (0, 72/255, 186/255),
                (135/255, 50/255, 96/255),
                (102/255, 255/255, 0),
                (153/255, 51/255, 0),
                (253/255, 238/255, 0)
                ]
    
        
    agents_list = []
    
    first_points = convert_str2tup(MAIN_LIST[1])
    i = 1
    print(i)
    single_log = MAIN_LIST[i]
    print(single_log)
    time = single_log.split()[0]
    states = convert_str2tup(single_log)
    
    # update properties
    color_ind = 1
    count = 0
    
    for coordinate in states:
        
        new_x = coordinate[0]
        new_y = coordinate[1]
        new_z = coordinate[2]
        obst = True if coordinate[3] == 2 else False
        
        if obst:
            color_ = color.white
            agents_list.append(sphere(color = color_,texture=textures.rock,
                                  radius = Radius,pos = vector(new_x,new_y,new_z)))            
        else:
            color_ = color_list[color_ind % min(len(color_list), num)]
            #print(color_)
            agents_list.append(sphere(color = vector(color_[0],color_[1],color_[2]),
                                  radius = Radius,pos = vector(new_x,new_y,new_z)))
            

        color_ind += 1   
    
    return agents_list


# In[10]:


def main():
    global running, obst_indx
    
    parser = argparse.ArgumentParser(description="Help for run simulator",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inputfile", help="get input file")
    parser.add_argument("-s", "--interval_speed", help="interval speed", default=1)
    parser.add_argument("-r", "--agent_radius", help="set agent radius", default=5)

    args = parser.parse_args()
    config = vars(args)
    print(config)


    #initialize global vars
    interval_speed = float(config['interval_speed'])
    LOG_FILE = config['inputfile']
    MAIN_LIST = read_log(LOG_FILE)
    RADIUS = float(config['agent_radius'])
    print('r is : ',RADIUS)
    Surface = []


    AGENT_NUMBER = int(MAIN_LIST[0])
    


    if AGENT_NUMBER == 0:
        raise EXCEPTION("YOUR NUMBER OF AGENTS IS ZERO !!")
    

    #start plot
    agents = build_agents(AGENT_NUMBER,MAIN_LIST,RADIUS)
    
    i = 2
    while i != len(MAIN_LIST):
        sleep(rate_slider.value)
        if running:
            print(i)
            single_log = MAIN_LIST[i]
            print(single_log)
            time = single_log.split()[0]
            states = convert_str2tup(single_log)
            time_text.text = 'travel time = {}'.format(time)


            all_positions = []

            # update properties
            color_ind = 1
            count = 0
            for coordinate in states:
                new_x = coordinate[0]
                new_y = coordinate[1]
                new_z = coordinate[2]
                
                if coordinate[3]==2:
                    obst_indx.append(len(all_positions))

                all_positions.append((new_x, new_y, new_z))
                agents[count].pos = vector(new_x, new_y, new_z)
                count += 1

            collisions_points = check_collision(all_positions, RADIUS)

            if not len(collisions_points) == 0:
                print("--COLLISION NUMBER : {} \nCOLLISION BETWEEN {}--".format(len(collisions_points), collisions_points)+bcolors.ENDC)
                time_text.text = ("COLLISTION")  
            i += 1
        


# In[11]:


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




