#!/usr/bin/env python

from lib2to3.pgen2.token import STAR
from django.shortcuts import redirect
import rvo23d
from matplotlib import animation
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from math import sqrt
from hungarian import find_minimum_match
import parameters


def distance_between(first, second):
      return sqrt((first[0]-second[0]) ** 2 + (first[1]-second[1]) ** 2 + (first[2]-second[2]) ** 2)

def find_distance_table(start_points, end_points):
      table = []
      for i in start_points:
            row = []
            for j in end_points:
                  row.append(distance_between(i, j))
            table.append(row)
      return table

def find_hungarian_match(start_points, end_points, matrix):
      start_ans = []
      end_ans = []
      for i in range(len(start_points)):
            flag = 0
            for j in range(len(end_points)):
                  if not matrix[i][j] == 0:
                        start_ans.append(start_points[i])
                        end_ans.append(end_points[j])
                        flag = 1
                        break

            if flag == 0:
                  # because start point and end point is same
                  # so in this row all points in matrix is 0
                  # finally we can add same point to start and end answer points

                  start_ans.append(start_points[i])
                  end_ans.append(start_points[i])

      return start_ans, end_ans


def absSq(vector):
      return sum([x*y for x,y in zip(vector, vector)])

def normalize(vector):
      denominator = sqrt(sum([x*y for x,y in zip(vector, vector)]))
      return tuple([x/denominator for x in vector])


def check_collision(all_positions, radius):
    collisions = []
    for i in range(len(all_positions)):
        for j in range(len(all_positions)):
            if i == j:
                continue
            distance = distance_between(all_positions[i], all_positions[j])
            if distance <= 2*radius:
                collisions.append((all_positions[i], all_positions[j]))
    return collisions







def main():

    print(parameters.startPoints)
    ########## this information must read from input file
    # timeStep = 20/20.
    # neighborDist = 1.5
    # maxNeighbors = 5
    # timeHorizon = 1.5
    # radius = 100
    # maxSpeed = 1
    # velocity = (1, 1, 1)




    # GOAL_POINTS= [
    #     #   (2034.2 ,-184.0 ,0.000),
    #     # (1664.4, 842.5 ,0.000),
    #     # (774.4, 1425.3 ,0.000),
    #     #  ( -271.3, 1425.3 ,0.000),
    #     #  ( -1161.3, 842.5 ,0.000),
    #     #   (-1531.1, -184.0 ,0.000),
    #     #   (-1161.3 ,-1210.5 ,0.000),
    #     #   (-271.3 ,-1793.2 ,0.000),
    #     #  ( 774.4 ,-1793.2 ,0.000),
    #     #   (1664.4 ,-1210.5 ,0.000)

    
    # # (-40, 40, -10),
    # # (-40, 20, -10),
    # # (40, -40, 10),
    # # (40, -20, 10)

    #     (1,0,0),
    #     (0,0,0)
    #  ]

    # START_POINTS = [
    #     # (-529.8, 244.2, 0.000),
    #     # (370.4 ,244.2 , 0.000),
    #     # (370.4 ,-110.9, 0.000),
    #     # (-529.8, -110.9,0.000),
    #     # (-229.7, 244.2, 0.000),
    #     # (-229.7, -110.9,0.000),
    #     # (70.4 ,244.2 , 0.000),
    #     # (70.4 ,-110.9, 0.000),
    #     # (-529.8, 066.7, 0.000),
    #     # (370.4 ,066.7 , 0.000)

    #     # (50, 20, 0),
    #     # (50, 40, 0),
    #     # (-50, 20, 0),
    #     # (-50, 40, 0)

    #     (1,0,0),
    #     (0,0,0)
    # ]
    # AGENTS = []
    # AGENT_NUMBER = 2
    # X_MAX = 100
    # Y_MAX = 100
    # Z_MAX = 100
    # X_MIN = -100
    # Y_MIN = -100
    # Z_MIN = -100

    ########## this information must read from input file




    ################## Hungarian algorithm ##################
    
    matrix = find_distance_table(parameters.startPoints, parameters.goalPoints)
    print("Matrix of distances :")
    print(matrix)
    sum, hung_ans = find_minimum_match(matrix)
    print("\nOutput of Hungarian algorithm : ")
    print(sum, hung_ans)
    parameters.startPoints, parameters.goalPoints = find_hungarian_match(parameters.startPoints, parameters.goalPoints, hung_ans)
    print("\nResult matching start and end points : ")
    print(parameters.startPoints, parameters.goalPoints)

    
    ################## simulator ##################

    fig = plt.figure()
    ax = p3.Axes3D(fig)
    txt = fig.suptitle('')
    


    #limit x & y & z
    ax.set_xlim(parameters.xMin,parameters.xMax)
    ax.set_ylim(parameters.yMin,parameters.yMax)
    ax.set_zlim(parameters.zMin,parameters.zMax)

    #initial points
    array_points = []
    for p in parameters.startPoints:
        new_poin, = ax.plot([p[0]],[p[1]],[p[2]],'o', markersize= parameters.radius)
        array_points.append(new_poin)

    #handel pausd and speed 
    anim_running = True
    interval_speed = 1
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



    ################## algorithm ##################
    sim = rvo23d.PyRVOSimulator(parameters.timeStep, parameters.neighborDist, parameters.maxNeighbors, parameters.timeHorizon, parameters.radius, parameters.maxSpeed, parameters.velocity)

    for i in range(parameters.agentNumber):
        new_agent =  sim.addAgent(parameters.startPoints[i], parameters.neighborDist, parameters.maxNeighbors, parameters.timeHorizon, parameters.radius, parameters.maxSpeed, (0, 0, 0))
        parameters.agent.append(new_agent)




    def set_preferred_velocities(): 
        for i in range(parameters.agentNumber):
                velocity_vector = tuple(x - y for x, y in zip (parameters.goalPoints[i], sim.getAgentPosition(i)))
                #print("velocity : " , GOAL_POINTS[i],sim.getAgentPosition(i),f"AGENT:{i}")
                #print(velocity_vector)
                if absSq(velocity_vector) > 1.0:
                    velocity_vector = normalize(velocity_vector)

                sim.setAgentPrefVelocity(i, velocity_vector)


    ## what is the end input here?
    # a0 = sim.addAgent((0, 0, 0), neighborDist, maxNeighbors, timeHorizon, radius, maxSpeed, (0, 0, 0))
    # a1 = sim.addAgent((1, 0, 0), neighborDist, maxNeighbors, timeHorizon, radius, maxSpeed, (0, 0, 0))
    # a2 = sim.addAgent((1, 1, 0), neighborDist, maxNeighbors, timeHorizon, radius, maxSpeed, (0, 0, 0))
    # a3 = sim.addAgent((0, 1, 0), neighborDist, maxNeighbors, timeHorizon, radius, maxSpeed, (0, 0, 0))


    # Set preferred velocities
    # sim.setAgentPrefVelocity(a0, (1, 1, 0))
    # sim.setAgentPrefVelocity(a1, (-1, 1, 0))
    # sim.setAgentPrefVelocity(a2, (-1, -1, 0))
    # sim.setAgentPrefVelocity(a3, (1, -1, 0))

    print('Simulation has %i agents in it.' %(sim.getNumAgents()))

    print('Running simulation')

    def reached_goal():
        for i in range(sim.getNumAgents()):
                if (absSq(x - y for x, y in zip (sim.getAgentPosition(i), parameters.goalPoints[i])) > 4 * sim.getAgentRadius(i) * sim.getAgentRadius(i)):
                    return False
        return True

    def counter():
        i = 0
        while(not reached_goal()):
                i += 1
                yield i


    def update_points(step, points,a):
        set_preferred_velocities()
        sim.doStep()
        txt.set_text('step : {} \ntravel time : {}'.format(step, sim.getGlobalTime()))
        print('step=%2i  t=%.3f' % (step, sim.getGlobalTime()))
        collisions_points = []
        all_positions = []
        for agent_no, point in zip(parameters.agent, points):

                new_position = sim.getAgentPosition(agent_no)
                positions = ['(%5.3f,%5.3f,%5.3f)' % new_position]
                print(new_position)
                new_x = new_position[0]
                new_y = new_position[1]
                new_z = new_position[2]
                point.set_data([new_x],[new_y])
                point.set_3d_properties([new_z], 'z')
                all_positions.append(new_position)


        collisions_points = check_collision(all_positions, parameters.radius)
        if not len(collisions_points) == 0:
            #txt.set_text("--COLLISION BETWEEN {}--".format(collisions_points))
            print("--COLLISION BETWEEN {}--".format(collisions_points))



    fig.canvas.mpl_connect('key_press_event', onClick)
    ani=animation.FuncAnimation(fig, update_points,
                            interval = interval_speed,
                            frames= counter,
                            repeat= False,
                            fargs= (array_points,1)
                            )
    
    #ani.save('../orca.mp4')
    print("=================End=================")

    plt.show()
    



if __name__ == "__main__":
    main()