/*
 * Agent.h
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

/**
 * \file    Agent.h
 * \brief   Contains the Agent class.
 */
#ifndef RVO_AGENT_H_
#define RVO_AGENT_H_

#include "API.h"
//#include "Barrier.h"

#include <cstddef>
#include <utility>
#include <vector>

#include "Vector3.h"

namespace RVO {
	//class KdTree;
	/**
	 * \brief   Defines an agent in the simulation.
	 */
	 /**
  * \brief   Defines a plane.
  */
	class Plane {
	public:
		/**
		 * \brief   A point on the plane.
		 */
		Vector3 point;

		/**
		 * \brief   The normal to the plane.
		 */
		Vector3 normal;
	};


	class Agent {
	public:
		/**
		 * \brief   Constructs an agent instance.
		 * \param   sim  The simulator instance.
		 */
		explicit Agent();

		~Agent();

		/**
		 * \brief   Computes the new velocity of this agent.
		 */
		void computeNewVelocity();

		/**
		 * \brief   Inserts an agent neighbor into the set of neighbors of this agent.
		 * \param   agent    A pointer to the agent to be inserted.
		 * \param   rangeSq  The squared range around this agent.
		 */
		void insertAgentNeighbor(const Agent *agent, float &rangeSq);


		/// new
		/// update 
		void update();
		/// get global time
		float getGlobalTime() const;
		/// <compute neighbor>
		void computeNeighbors();
		/// defaults
		void setAgentDefaults(float neighborDist, size_t maxNeighbors, float timeHorizon, float radius, float maxSpeed, const Vector3& velocity);
		/// timestep
		void setTimeStep(float timeStep);
		/// run
		void run(std::vector<Agent*> agents);
		//pref_velocity
		void setAgentPrefVelocity(const Vector3& prefVelocity);
	
		/// new

		Vector3 newVelocity_;
		Vector3 position_;
		Vector3 prefVelocity_;
		Vector3 velocity_;
		Vector3 agent_goal;//new
		bool reached;

		//RVOSimulator *sim_;
		//new
		//KdTree* kdTree_; 1
		//new
		size_t id_;
		size_t maxNeighbors_;
		float maxSpeed_;
		float neighborDist_;
		float radius_;
		float timeHorizon_;
		/// <summary>
		float globalTime_;
		float timeStep_;
		/// </summary>
		std::vector<std::pair<float, const Agent *> > agentNeighbors_;
		std::vector<Agent*> tot_agents;
		std::vector<Plane> orcaPlanes_;

		//friend class KdTree; 1
		//friend class RVOSimulator;

		//barrier
		std::vector<Agent> barriers_;
		
		//barrier
	};
}

#endif /* RVO_AGENT_H_ */
