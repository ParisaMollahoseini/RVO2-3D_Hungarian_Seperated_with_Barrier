from functools import reduce
from timeit import repeat
from tkinter import EXCEPTION
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
from ast import literal_eval as make_tuple
from math import sqrt
import argparse

global count
count = 0

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


def read_log(file_name:str):
    f = open(file_name , 'r')
    f_lines = f.read().split('\n')
    f_lines.pop()
    f.close()
    return f_lines


def convert_str2tup(inp:str):
   list_of_tuple = [make_tuple(i) for i in inp.split()[1:]]
   return list_of_tuple

def distance_between(first, second):
      return sqrt((first[0]-second[0]) ** 2 + (first[1]-second[1]) ** 2 + (first[2]-second[2]) ** 2)

def check_collision(all_positions, radius):
    collisions = []
    for i in range(len(all_positions)):
        for j in range(len(all_positions)):
            if i == j:
                continue
            distance = distance_between(all_positions[i], all_positions[j])
            if distance < 2*radius:
                collisions.append((all_positions[i], all_positions[j]))
    return collisions





def main():

    parser = argparse.ArgumentParser(description="Help for run simulator",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inputfile", help="get input file")
    parser.add_argument("-s", "--interval_speed", help="set interval speed", default=10)
    parser.add_argument("-r", "--agent_reduce", help="set agent reduce", default=5)

    args = parser.parse_args()
    config = vars(args)
    print(config)


    #initialize global vars
    interval_speed = float(config['interval_speed'])
    LOG_FILE = config['inputfile']
    REDUCE = float(config['agent_reduce'])

    MAIN_LIST = read_log(LOG_FILE)

    #print("--------------")
    #print(MAIN_LIST)
    AGENT_NUMBER = MAIN_LIST[0]
    X_MAX = 100
    Y_MAX = 100
    Z_MAX = 100
    X_MIN = -100
    Y_MIN = -100
    Z_MIN = -100




    if AGENT_NUMBER == 0:
        raise EXCEPTION("YOUR NUMBER OF AGENTS IS ZERO !!")
    

    #start plot
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    #limit x & y & z
    ax.set_xlim(X_MIN,X_MAX)
    ax.set_ylim(Y_MIN,Y_MAX)
    ax.set_zlim(Z_MIN,Z_MAX)

    #initalize points
    first_points = convert_str2tup(MAIN_LIST[1])

    array_points = []
    for p in first_points:
        if p[3] == 1:
            new_poin, = ax.plot([p[0]],[p[1]],[p[2]],'o', color='r')
        else:
            new_poin, = ax.plot([p[0]],[p[1]],[p[2]],'s', color='k')

        array_points.append(new_poin)



   
    anim_running = True
    def onClick(event):
        print(event.key)
        #nonlocal interval_speed
        if event.key == 'enter':
            nonlocal anim_running
            if anim_running:
                ani.event_source.stop()
                anim_running = False
            else:
                ani.event_source.start()
                anim_running = True
        
        elif event.key == 'up':
            #interval_speed -= 100
            pass

        elif event.key == 'down':
            #interval_speed += 100
            pass

    txt = fig.suptitle('')
    def update_points(index, single_log, main_list, points):
        global count
        #in next version ====>>> comment next line and find single_log from input
        #print(index)
        single_log = main_list[index + 1]
        print(single_log)
        time = single_log.split()[0]
        states = convert_str2tup(single_log)
        txt.set_text('travel time = {}'.format(time)) 

        all_positions = []
        # update properties
        for point,coordinate in zip(points, states):

            new_x = coordinate[0]
            new_y = coordinate[1]
            new_z = coordinate[2]
            point.set_data(new_x,new_y)
            point.set_3d_properties(new_z, 'z')
            all_positions.append((new_x, new_y, new_z))

        collisions_points = check_collision(all_positions, REDUCE)
        count += len(collisions_points)
        if not len(collisions_points) == 0:
            #txt.set_text("--COLLISION BETWEEN {}--".format(collisions_points))
            print(bcolors.FAIL + "--COLLISION NUMBER : {} \nCOLLISION BETWEEN {}--".format(len(collisions_points), collisions_points) + bcolors.ENDC)
            txt.set_text("COLLISTION")
        return points,txt


    fig.canvas.mpl_connect('key_press_event', onClick)

    # in next version ====>>>>> set frames=100 for instance. because its not important
    ani=animation.FuncAnimation(fig, update_points,
                                interval = interval_speed,
                                frames=len(MAIN_LIST) - 1,
                                fargs=("", MAIN_LIST , array_points),
                                repeat= False
                                )
    # #pause
    # anim.event_source.stop()

    # #unpause
    # anim.event_source.start()

    #save gif
    writergif = animation.PillowWriter(fps=30) 
    ani.save('result.gif', writer=writergif)

    plt.show()
    print("THE END...",count)



if __name__ == "__main__":
    main()