/*
 * Sphere.cpp
 * RVO2-3D Library
 *
 * Copyright 2008 University of North Carolina at Chapel Hill
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Please send all bug reports to <geom@cs.unc.edu>.
 *
 * The authors may be contacted via:
 *
 * Jur van den Berg, Stephen J. Guy, Jamie Snape, Ming C. Lin, Dinesh Manocha
 * Dept. of Computer Science
 * 201 S. Columbia St.
 * Frederick P. Brooks, Jr. Computer Science Bldg.
 * Chapel Hill, N.C. 27599-3175
 * United States of America
 *
 * <http://gamma.cs.unc.edu/RVO2/>
 */

/* Example file showing a demo with 812 agents initially positioned evenly distributed on a sphere attempting to move to the antipodal position on the sphere. */

#ifndef RVO_OUTPUT_TIME_AND_POSITIONS
#define RVO_OUTPUT_TIME_AND_POSITIONS 1
#endif

#include <cmath>
#include <cstddef>
#include <vector>
#include <sstream>
#include "json.hpp"
#include <fstream>
#include "Vector3.h"
//#include "Barrier.h"
using json = nlohmann::json;

#if RVO_OUTPUT_TIME_AND_POSITIONS
#include <iostream>
#endif

#ifdef _OPENMP
#include <omp.h>
#endif


#include "RVO.h"
#include "Agent.h"
#include "Hungarian.h"

#ifndef M_PI
const float M_PI = 3.14159265358979323846f;
#endif

/* Store the goals of the agents. */
std::vector<RVO::Vector3> goals;
std::vector<RVO::Agent> barriers_;
std::vector<RVO::Agent*> agents_;
float time_step;
float globalTime_;
float radius_;

std::vector<std::vector<float>> startpoints, goalpoints;
float neighbordist, maxNeighbors, timeHorizon, maxSpeed;
RVO::Vector3 velocity;
char* file_name;
int num_agents;
// Hungarian

vector<vector<long double>> find_distance_table(int number_of_point, float x_start[], float y_start[], float z_start[], float x_goal[], float y_goal[], float z_goal[])
{

	vector<vector<long double>> distance_table(number_of_point, vector<long double>(number_of_point, 0));
	for (int i = 0; i < number_of_point; i++)
	{
		float x_s = x_start[i];
		float y_s = y_start[i];
		float z_s = z_start[i];

		for (int j = 0; j < number_of_point; j++)
		{
			float x_g = x_goal[j];
			float y_g = y_goal[j];
			float z_g = z_goal[j];

			long double distance = sqrt(pow((x_s - x_g), 2) + pow((y_s - y_g), 2) + pow((z_s - z_g), 2));
			distance_table[i][j] = distance;
			//cout << distance<< "\t";

		}
		//cout << endl;
	}


	return distance_table;

}

void change_order_of_goals(int number_of_point, vector<int> assignment, float x_goal[], float y_goal[], float z_goal[])
{

	float* x_goal_copy = new float[number_of_point];
	float* y_goal_copy = new float[number_of_point];
	float* z_goal_copy = new float[number_of_point];
	for (int i = 0; i < number_of_point; i++)
	{
		x_goal_copy[i] = x_goal[i];
		y_goal_copy[i] = y_goal[i];
		z_goal_copy[i] = z_goal[i];
	}

	for (unsigned int x = 0; x < number_of_point; x++)
	{
		int best_goal_index = assignment[x];

		//call by refrence:)
		x_goal[x] = x_goal_copy[best_goal_index];
		y_goal[x] = y_goal_copy[best_goal_index];
		z_goal[x] = z_goal_copy[best_goal_index];
	}
	delete[] x_goal_copy;
	delete[] y_goal_copy;
	delete[] z_goal_copy;

}

// Hungarian

void addAgent(const RVO::Vector3& position, RVO::Vector3 goal, std::vector<RVO::Agent> bar)
{
	RVO::Agent* agent = new RVO::Agent();

	agent->position_ = position;
	float this_neighborDist, this_maxNeighbors, this_timeHorizon, this_radius, this_maxSpeed;
	RVO::Vector3 this_velocity;

	if (neighbordist != -1)
		this_neighborDist = neighbordist;
	else
		this_neighborDist = 100.0f;

	if (maxNeighbors != -1)
		this_maxNeighbors = maxNeighbors;
	else
		this_maxNeighbors = 10;

	if (timeHorizon != -1)
		this_timeHorizon = timeHorizon;
	else
		this_timeHorizon = 10;

	if (radius_ != -1)
		this_radius = radius_;
	else
		this_radius = 1.5f;

	if (maxSpeed != -1)
		this_maxSpeed = maxSpeed;
	else
		this_maxSpeed = 2.0f;

	if (velocity != RVO::Vector3(0, 0, 0))
		this_velocity = velocity;
	else
		this_velocity = RVO::Vector3(0, 0, 0);

	agent->setAgentDefaults(this_neighborDist,this_maxNeighbors, this_timeHorizon, this_radius,
		this_maxSpeed,this_velocity);//velocity
	
	agent->id_ = agents_.size()+barriers_.size();
	/* Specify the global time step of the simulation. */
	agent->setTimeStep(1.0f);

	agent->agent_goal = goal;

	copy(bar.begin(), bar.end(), back_inserter(agent->barriers_));
	agents_.push_back(agent);

}

void setupScenario()
{
	//read barrier file
	std::string text;
	std::ifstream BarFile("barrier.txt");
	

	while (getline(BarFile, text)) {
		std::stringstream   lineStream(text);    // convert your line into a stream.
		int type;
		float  x, y, z, vx, vy, vz;
		if (lineStream >> type)
		{
			//std::cout << "type is: " << type;
			if (type == 0)
			{
				if (lineStream >> x >> y >> z)
				{
					RVO::Agent bar;
					bar.setAgentDefaults(15.0f, -1, 10.0f, radius_, 2.0f, RVO::Vector3(0, 0, 0));//velocity
					bar.id_ = barriers_.size();
					bar.position_ = RVO::Vector3(x, y, z);
					
					barriers_.push_back(bar);
					//std::cout << "Barrier is: " << x << "," << y << "," << z << std::endl;
					// Read all the values successfully
				}
			}
			else if (type == 1)
			{
				if (lineStream >> x >> y >> z >> vx >> vy >> vz)
				{
					RVO::Agent bar;
					bar.setAgentDefaults(15.0f, -1, 10.0f, radius_, 2.0f, RVO::Vector3(vx, vy, vz));//velocity
					bar.id_ = barriers_.size();
					bar.position_ = RVO::Vector3(x, y, z);
					
					barriers_.push_back(bar);
					//std::cout << "Barrier is: " << x << "," << y << "," << z << "," << vx << "," << vy << "," << vz << std::endl;
					// Read all the values successfully
				}
			}
		}
		
	}

	// Close the file
	BarFile.close();
	//read barrier file


	time_step = 1.0f;
	globalTime_ = 0;

	//int num = 12;
	//float x_list[12] = { 36.0 ,30.0 ,16.0 ,-2.1,-20.0,-35.0,-40.0,-35.0 ,-20.0,-2.1,16.0,30.6 };//, -3.0, -3.0, -30.7, 30.1};//
	//float y_list[12] = { 5.0 ,22.4 , 34.0, 37.7 ,34.0,22.4, 5.0, -12.4, -24.0 ,-27.7 ,-24.0 ,-12.4 };// , 20.8, -10.5, 6.0, 6.0 };//};
	//float z_list[12] = { 0,0,0,0,0,0,0,0 ,0,0,0,0 };
	//float x_goal_list[12] = { -60.0 ,52.3 ,52.3,-60.0,-32.0,-32.0,-4.0,-4.0, 24.2, 24.2, -60.0, 52.3 };// , -30.4, -20.5, -5, 10.4};// };
	//float y_goal_list[12] = { 34.4,34.4,-20.0,-20.0,34.4,-20.0,34.4,-20.0,34.4,-20.0,7.2,7.2 };//,3.0,-10.5,-20.2,-10.5 };//};
	//float z_goal_list[12] = { 0,0,0,0,0,0,0,0 ,0,0,0,0 };

	////Hungarian

	//vector< vector<double> > costMatrix = find_distance_table(num, x_list, y_list, z_list, x_goal_list, y_goal_list, z_goal_list);

	//HungarianAlgorithm HungAlgo;
	//vector<int> assignment;

	//double cost = HungAlgo.Solve(costMatrix, assignment);
	//change_order_of_goals(num, assignment, x_goal_list, y_goal_list, z_goal_list);
	//// Hungarian

	//for (int i = 0; i < num; i++)
	//{
	//	RVO::Vector3 pos = RVO::Vector3(x_list[i], y_list[i], z_list[i]);
	//	RVO::Vector3 goal = RVO::Vector3(x_goal_list[i], y_goal_list[i], z_goal_list[i]);
	//	addAgent(pos, goal, barriers_);

	//	goals.push_back(goal);
	//}
	/// Sphere
	//float *x_list, *y_list, *z_list, *x_goal_list, *y_goal_list, *z_goal_list;

	//x_list = new float[812];
	//y_list = new float[812];
	//z_list = new float[812];

	//x_goal_list = new float[812];
	//y_goal_list = new float[812];
	//z_goal_list = new float[812];

	//int count = 0;

	//for (float a = 0; a < M_PI; a += 0.1f) {
	//	const float z = 100.0f * std::cos(a);
	//	const float r = 100.0f * std::sin(a);

	//	for (size_t i = 0; i < r / 2.5f; ++i) {
	//		const float x = r * std::cos(i * 2.0f * M_PI / (r / 2.5f));
	//		const float y = r * std::sin(i * 2.0f * M_PI / (r / 2.5f));

	//		x_list[count] = x;
	//		y_list[count] = y;
	//		z_list[count] = z;

	//		x_goal_list[count] = -x;
	//		y_goal_list[count] = -y;
	//		z_goal_list[count] = -z;
	//		count += 1;

	//	}
	//}
	////std::cout << "count\n";
	//// Hungarian
	//int num = 812;
	//vector< vector<long double> > costMatrix = find_distance_table(num, x_list, y_list, z_list, x_goal_list, y_goal_list, z_goal_list);

	//HungarianAlgorithm HungAlgo;
	//vector<int> assignment;
	////std::cout << "count\n";
	//double cost = HungAlgo.Solve(costMatrix, assignment);
	////std::cout << "count\n";
	//change_order_of_goals(num, assignment, x_goal_list, y_goal_list, z_goal_list);
	//
	//// Hungarian
	//for (int k = 0; k < num; k++)
	//{

	//	addAgent(RVO::Vector3(x_list[k], y_list[k], z_list[k]), RVO::Vector3(x_goal_list[k], y_goal_list[k], z_goal_list[k]), barriers_);

	//	goals.push_back(RVO::Vector3(x_goal_list[k], y_goal_list[k], z_goal_list[k]));
	//}
	//delete[] x_list;
	//delete[] y_list;
	//delete[] z_list;

	//delete[] x_goal_list;
	//delete[] y_goal_list;
	//delete[] z_goal_list;
	/// Sphere

	/// text to sphere
	float *x_list, *y_list, *z_list, *x_goal_list, *y_goal_list, *z_goal_list;

	x_list = new float[num_agents];
	y_list = new float[num_agents];
	z_list = new float[num_agents];

	x_goal_list = new float[num_agents];
	y_goal_list = new float[num_agents];
	z_goal_list = new float[num_agents];

	for (int i = 0; i < num_agents; i++)
	{
		x_list[i] = startpoints[i][0];
		y_list[i] = startpoints[i][1];
		z_list[i] = startpoints[i][2];

		x_goal_list[i] = goalpoints[i][0];
		y_goal_list[i] = goalpoints[i][1];
		z_goal_list[i] = goalpoints[i][2];
	}
	//float x_goal_list[20] = { 19.0 ,19.15 ,16.61 ,18.92,15.83,17.5,13.28,11.95 ,14.56, 15.83, 11.95, 10.5, 7.34, 8.57, 8.10741, 10.29019, 0.17, 5.87, 3.51, 3.51};//20
	//float y_goal_list[20] = { -0.98729, -0.21, -1.32, -3.69, -3.69, -5.42, -2.95, -4.49, -4.49, 0, 0, -2.11, -2.11, -3.81, -0.91222, -1.21795, -5.94, -5.94, -5.94, 0};
	//float z_goal_list[20] = { 0,0,0,0,0,0,0,0 ,0,0,0,0 ,0,0,0,0 ,0,0,0,0 };
	//
	//float x_list[20] = { 5.30196, -2, 2, 9.60788, 2, -6, 2, -10, -7.7588, 10, 9.60788, 2, -2, 6, -9.60788, 2, 6, 2, 2, 6};
	//float y_list[20] = { 2, 6, 9.60788, 2, -2, -2, -9.60788, 5.30196, 6, -2, -6, 9.60788, -11.15109, -6, -6, 5.30196, -9.60788, -11.15109, -2,  -9.60788};
	//float z_list[20] = { 10, 9.60788, 6, 6, 11.15109, 9.60788, 6, 2, -6, 5.30196, -2, -6, -2, -7.7588, -2, -10, -2, 2, -11.15109, 2 };
	
	//Hungarian
	//for (int k = 0; k < num_agents; k++)
	//{
	//	x_goal_list[k] = x_goal_list[k] * 10;
	//	y_goal_list[k] = y_goal_list[k] * 10;
	//	z_goal_list[k] = z_goal_list[k] * 10;

	//	x_list[k] = x_list[k] * 10;
	//	y_list[k] = y_list[k] * 10;
	//	z_list[k] = z_list[k] * 10;
	//}
	vector< vector<long double> > costMatrix = find_distance_table(num_agents, x_list, y_list, z_list, x_goal_list, y_goal_list, z_goal_list);

	HungarianAlgorithm HungAlgo;
	vector<int> assignment;

	double cost = HungAlgo.Solve(costMatrix, assignment);
	change_order_of_goals(num_agents, assignment, x_goal_list, y_goal_list, z_goal_list);
	// Hungarian

	for (int i = 0; i < num_agents; i++)
	{
		RVO::Vector3 pos = RVO::Vector3(x_list[i], y_list[i], z_list[i]);
		RVO::Vector3 goal = RVO::Vector3(x_goal_list[i], y_goal_list[i], z_goal_list[i]);
		addAgent(pos, goal, barriers_);

		goals.push_back(goal);
	}
}

#if RVO_OUTPUT_TIME_AND_POSITIONS
void updateVisualization()
{

	std::cout << globalTime_;
	globalTime_ += time_step;

	/* Output the position for all the agents. */
	//std::cout << " 1";
	for (size_t i = 0; i < agents_.size(); ++i) { 
		std::cout << " (" << agents_[i]->position_.x()<<","<< agents_[i]->position_.y() << "," << agents_[i]->position_.z() << "," << "1)";
	}
	//std::cout << " 2";
	for (size_t i = 0; i < barriers_.size(); ++i) {
		std::cout << " (" << agents_[2]->barriers_[i].position_.x() << "," << agents_[2]->barriers_[i].position_.y() << "," << agents_[2]->barriers_[i].position_.z() << "," << "2)";

	}

	std::cout << std::endl;
}
#endif

void setPreferredVelocities()
{
	/* Set the preferred velocity to be a vector of unit magnitude (speed) in the direction of the goal. */
	for (size_t i = 0; i < agents_.size(); ++i) {

		RVO::Vector3 goalVector = goals[i] - agents_[i]->position_;

		if (RVO::absSq(goalVector) > 1.0f) {
			goalVector = RVO::normalize(goalVector);
		}
		agents_[i]->setAgentPrefVelocity(goalVector);
	}
}


int main(int argc, char** argv)
{
	if (argc > 1)
	{
		file_name = argv[1];
	}


	std::ifstream f(file_name);
	json data = json::parse(f);

	num_agents = data["startPoints"].size();
	data["startPoints"].get_to(startpoints);
	data["goalPoints"].get_to(goalpoints);
	time_step = data["timeStep"];
	neighbordist = data["neighborDist"];
	maxNeighbors = data["maxNeighbors"];
	timeHorizon = data["timeHorizon"];
	radius_ = data["radius"];
	maxSpeed = data["maxSpeed"];
	velocity = RVO::Vector3(data["velocity_x"], data["velocity_y"], data["velocity_z"]);

	/* Set up the scenario. */

	setupScenario();

	/* Perform (and manipulate) the simulation. */
	std::cout << agents_.size()+barriers_.size() << std::endl;
	int count = 0;

#if RVO_OUTPUT_TIME_AND_POSITIONS
	updateVisualization();
#endif
	setPreferredVelocities();

	while (count < agents_.size())
	{

#ifdef _OPENMP
#pragma omp parallel for
#endif
		for (int j = 0; j < agents_.size(); j++)
		{
			//std::cout << agents_[j]->reached <<"hi\n";
			agents_[j]->run(agents_);
			//if (agents_[j]->reached == false)
			//{
			//	//std::cout << agents_[j]->id_ << " run \n";
			//	agents_[j]->run(agents_);
			//	
			//	//std::cout << " run \n";

			//}
		}
#ifdef _OPENMP
#pragma omp parallel for
#endif
		for (int j = 0; j < agents_.size(); j++)
		{
			agents_[j]->update();

			//if (agents_[j]->reached == false)
			//{
			//	agents_[j]->update();
			//	if (agents_[j]->reached == true)
			//	{
			//		//std::cout << "------ agent[" << agents_[j]->id_ << "] reached -----\n";
			//		count += 1;
			//	}
			//}
		}

#if RVO_OUTPUT_TIME_AND_POSITIONS
		updateVisualization();
#endif
		setPreferredVelocities();

		count = 0;
		for (int i = 0; i < agents_.size(); i++) {

			if (agents_[i]->reached == true)
			{
				//std::cout << "------ agent[" << agents_[j]->id_ << "] reached -----\n";
				count += 1;
			}
		}
	}
	//std::cout << "count\n";
	for (int j = 0; j < agents_.size(); j++)
	{
		delete agents_[j];
	}
	
	return 0;
}


//float x_list[4] = { -55.91 ,55.34 ,55.34 ,-55.91 };//, -3.0, -3.0, -30.7, 30.1};//
//float y_list[4] = { 40.98 ,40.98,-37.02,-37.02 };// , 20.8, -10.5, 6.0, 6.0 };//};
//float z_list[4] = { 0,0,0,0 };

//float x_goal_list[4] = { 48.09 ,-3.16 ,-54.41,-3.16 };// , -30.4, -20.5, -5, 10.4};// };
//float y_goal_list[4] = { -1.64 ,39.98, -1.64,-43.27 };//,3.0,-10.5,-20.2,-10.5 };//};
//float z_goal_list[4] = { 0,0,0,0 };


//float x_list[12] = { 36.0 ,30.0 ,16.0 ,-2.1,-20.0,-35.0,-40.0, -35.0 ,-20.0,-2.1,16.0,30.6 };//, -3.0, -3.0, -30.7, 30.1};//
//float y_list[12] = { 5.0 ,22.4 ,34.0,37.7 ,34.0,22.4,5.0,-12.4,-24.0 ,-27.7 ,-24.0 ,-12.4 };// , 20.8, -10.5, 6.0, 6.0 };//};
//float z_list[12] = { 0,0,0,0,0,0,0,0 ,0,0,0,0 };
//float x_goal_list[12] = { -60.0 ,52.3 ,52.3,-60.0,-32.0,-32.0,-4.0,-4.0, 24.2, 24.2, -60.0, 52.3 };// , -30.4, -20.5, -5, 10.4};// };
//float y_goal_list[12] = { 34.4,34.4,-20.0,-20.0,34.4,-20.0,34.4,-20.0,34.4,-20.0,7.2,7.2 };//,3.0,-10.5,-20.2,-10.5 };//};
//float z_goal_list[12] = { 0,0,0,0,0,0,0,0 ,0,0,0,0 };

//334.1584, -16.807, 0 23.74

	/* Add agents, specifying their start position, and store their goals on the opposite side of the environment. */
//for (float a = 0; a < M_PI; a += 0.1f) {
//	const float z = 100.0f * std::cos(a);
//	const float r = 100.0f * std::sin(a);

//	for (size_t i = 0; i < r / 2.5f; ++i) {
//		const float x = r * std::cos(i * 2.0f * M_PI / (r / 2.5f));
//		const float y = r * std::sin(i * 2.0f * M_PI / (r / 2.5f));


//		RVO::Vector3 pos = RVO::Vector3(x, y, z);
//		RVO::Vector3 goal = RVO::Vector3(-pos);
//		addAgent(pos, goal, barriers_);

//		goals.push_back(goal);
//	}
//}
//float x_list[4] = { -40 ,-40 ,40,40 };//, -3.0, -3.0, -30.7, 30.1};//
//float y_list[4] = { 40 ,20,-40,-20 };// , 20.8, -10.5, 6.0, 6.0 };//};
//float z_list[4] = { -10,-10,10,10 };

//float x_goal_list[4] = { 50,50,-50,-50};// , -30.4, -20.5, -5, 10.4};// };
//float y_goal_list[4] = { 20,40,20,40 };//,3.0,-10.5,-20.2,-10.5 };//};
//float z_goal_list[4] = { 0,0,0,0 };
// 
//float x_list[10] = { -40,-40,-40,-40,-40,40,40,40,40,40 };//, -3.0, -3.0, -30.7, 30.1};//
//float y_list[10] = { 40,20,0,-20,-40,-40,-20,0,20,40 };// , 20.8, -10.5, 6.0, 6.0 };//};
//float z_list[10] = { 0,0,0,0,0,0,0,0,0,0 };

//float x_goal_list[10] = { 120 ,90 ,60,30,0,-30,-60,-90,-120,-150 };// , -30.4, -20.5, -5, 10.4};// };
//float y_goal_list[10] = { -10,-10, -10, -10, -10, -10, -10, -10, -10, -10};//,3.0,-10.5,-20.2,-10.5 };//};
//float z_goal_list[10] = { 0,0,0,0,0,0,0,0,0,0 };

//float x_list[12] = { 36.0 ,30.0 ,16.0 ,-2.1,-20.0,-35.0,-40.0, -35.0 ,-20.0,-2.1,16.0,30.6 };//, -3.0, -3.0, -30.7, 30.1};//
//float y_list[12] = { 5.0 ,22.4 ,34.0,37.7 ,34.0,22.4,5.0,-12.4,-24.0 ,-27.7 ,-24.0 ,-12.4 };// , 20.8, -10.5, 6.0, 6.0 };//};
//float x_goal_list[12] = { -60.0 ,52.3 ,52.3,-60.0,-32.0,-32.0,-4.0,-4.0, 24.2, 24.2, -60.0, 52.3 };// , -30.4, -20.5, -5, 10.4};// };
//float y_goal_list[12] = { 34.4,34.4,-20.0,-20.0,34.4,-20.0,34.4,-20.0,34.4,-20.0,7.2,7.2 };//,3.0,-10.5,-20.2,-10.5 };//};


/* circle 12
3.659 0.498 0.000
3.063 2.244 0.000
1.604 3.390 0.000
-0.216 3.773 0.000
-2.035 3.390 0.000
-3.495 2.244 0.000
-4.091 0.498 0.000
-3.495 -1.247 0.000
-2.035 -2.393 0.000
-0.216 -2.777 0.000
1.604 -2.393 0.000
3.063 -1.247 0.000
*/

// square 4
/*
-5.591 4.098 0.000
5.534 4.098 0.000
5.534 -3.702 0.000
-5.591 -3.702 0.000
*/

/* circle 4
4.809 -0.164 0.000
-0.316 3.998 0.000
-5.441 -0.164 0.000
-0.316 -4.327 0.000

*/
/* circle 8
0.309 1.623 0.000
-0.515 3.176 0.000
-2.216 3.723 0.000
-3.916 3.176 0.000
-4.741 1.623 0.000
-3.916 0.071 0.000
-2.216 -0.477 0.000
-0.515 0.071 0.000
*/
/* square 8
-5.216 3.623 0.000
5.434 3.623 0.000
5.434 -2.402 0.000
-5.216 -2.402 0.000
0.109 3.623 0.000
0.109 -2.402 0.000
-5.216 0.611 0.000
5.434 0.611 0.000
*/
/* square 12
-6.016 3.448 0.000
5.234 3.448 0.000
5.234 -2.002 0.000
-6.016 -2.002 0.000
-3.203 3.448 0.000
-3.203 -2.002 0.000
-0.391 3.448 0.000
-0.391 -2.002 0.000
2.422 3.448 0.000
2.422 -2.002 0.000
-6.016 0.723 0.000
5.234 0.723 0.000
*/




	/* Add agents, specifying their start position, and store their goals on the opposite side of the environment.
	for (float a = 0; a < M_PI; a += 0.1f) {
		const float z = 100.0f * std::cos(a);
		const float r = 100.0f * std::sin(a);

		for (size_t i = 0; i < r / 2.5f; ++i) {
			const float x = r * std::cos(i * 2.0f * M_PI / (r / 2.5f));
			const float y = r * std::sin(i * 2.0f * M_PI / (r / 2.5f));

			RVO::Vector3 pos = RVO::Vector3(x, y, z);
			addAgent(pos, -pos);

			goals.push_back(-pos);
		}
	}*/



	/* Output the current global time. */
	//for (int i = 0; i < agents_.size(); i++)
	//{
	//	if (agents_[i].reached == false) {
	//	std::cout << i << ": "<<agents_[i].getGlobalTime() << std::endl;
	//	std::cout << "position: " << agents_[i].position_ << std::endl;
	//	}
	//	
	//}
	//std::cout << "--------------------------------------------------\n";
	//std::cout << std::endl;

	/* Output the current global time. */