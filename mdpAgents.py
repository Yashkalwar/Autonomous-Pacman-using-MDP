# -*- coding: utf-8 -*-

# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py


# AI REASONING AND DECISION MAKING Coursework 
# YASH KALWAR 
# MSc Artificial Intelligence
# K24018103
#
# Code has been referenced from:
# [1] https://prateek-mishra.medium.com/markovian-pac-man-8dd212c5a35c
# [2] https://medium.com/@ngao7/markov-decision-process-value-iteration-2d161d50a6ff
# [3] https://youtu.be/3DxXFWsHpvU?si=l08h9QiAUU22t60l pacman problem video by audacity
# [4] https://courses.cs.washington.edu/courses/cse573/17wi/pacman/ps3/mdp.html
# [5] https://github.com/eamansour/pacman/blob/main/mdpAgents.py
# [6] https://github.com/DarrenSandhu/Pacman-Markov-Decision-Process

from pacman import Directions
import api
import random

class MDPAgent:
    def __init__(self):
        #Set the rewards for food,empty,ghost,capsule,scaredGhost 
        self.FOOD_REWARD = 370.0
        self.EMPTY_REWARD = -0.9
        self.GHOST_REWARD = -500.0
        self.CAPSULE_REWARD = 800.0
        self.SCARED_GHOST_REWARD = 5000.0
        
        # constant values for Markov value iteration
        self.discount = 0.85
        self.iteration_count = 15
        
        # initialising state variables
        self.walls = set()
        self.rewards = {}
        self.utilities = {}
        self.grid = {}
        self.first_move = True
        self.previous_action = None

    def initializeGameBoard(self, state):
        # Get wall positions from the game state
        walls = api.walls(state)
        self.walls = set(walls)
        
        # Find the dimensions of the game board
        max_x = max(pos[0] for pos in walls)
        max_y = max(pos[1] for pos in walls)
        
        # Initialize grid with empty rewards
        # Iterate through each position on the board
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                current_position = (x, y)
                
                # If position is not a wall, assign empty space reward
                if current_position not in self.walls:
                    self.grid[current_position] = self.EMPTY_REWARD

    def calculateDistance(self, pos1, pos2): #manhattan distance
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Calculate horizontal and vertical distances
        horizontal_distance = abs(x2 - x1)
        vertical_distance = abs(y2 - y1)
        
        # Return total Manhattan distance
        return horizontal_distance + vertical_distance

    def predictNextPosition(self, pos, action):
        # movement vector for each direction and if its wall then return current position otherwise next position
        directions = {
            Directions.NORTH: (0, 1),   # Move up
            Directions.SOUTH: (0, -1),  # Move down
            Directions.EAST: (1, 0),    # Move right
            Directions.WEST: (-1, 0)    # Move left
        }
        
        # Get the movement vector for the given action
        dx, dy = directions[action]
        
        # Calculate the next position
        next_pos = (pos[0] + dx, pos[1] + dy)
        
        # Check if the next position is valid (not a wall)
        if next_pos in self.walls:
            return pos  
            
        return next_pos  

    def getPossibleOutcomes(self, pos, action):
        """Get successor states and their probabilities"""
        x, y = pos
        dx, dy = {
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1),
            Directions.EAST: (1, 0),
            Directions.WEST: (-1, 0)
        }[action]

        # Main direction (80% probability)
        next_pos = (x + dx, y + dy)
        successors = [(next_pos if next_pos not in self.walls else pos, 0.8)]

        # Side directions (10% probability each)
        if dx == 0:  # Moving North/South
            side_positions = [
                ((x + 1, y) if (x + 1, y) not in self.walls else pos, 0.1),
                ((x - 1, y) if (x - 1, y) not in self.walls else pos, 0.1)
            ]
        else:  # Moving East/West
            side_positions = [
                ((x, y + 1) if (x, y + 1) not in self.walls else pos, 0.1),
                ((x, y - 1) if (x, y - 1) not in self.walls else pos, 0.1)
            ]
        
        successors.extend(side_positions)
        return successors

    def refreshGhostValues(self, state):
        """Update rewards based on ghost positions"""
        
        # Reset and initialize grid
        food_positions = api.food(state)
        capsule_positions = api.capsules(state)
        
        # Reset all positions to empty first
        for pos in self.grid:
            if pos not in self.walls:
                self.grid[pos] = self.EMPTY_REWARD

        # Set food rewards
        for food_pos in food_positions:
            self.grid[food_pos] = self.FOOD_REWARD

        # Set capsule rewards
        for capsule_pos in capsule_positions:
            self.grid[capsule_pos] = self.CAPSULE_REWARD

        # Handling ghosts
        for ghost_state in api.ghostStatesWithTimes(state):
            ghost_pos = (int(ghost_state[0][0]), int(ghost_state[0][1]))
            timer = ghost_state[1]
            
            if timer > 0:  # Scared ghost
                self.grid[ghost_pos] = self.SCARED_GHOST_REWARD * (timer / 40.0)
            else:  # Normal ghost
                self.grid[ghost_pos] = self.GHOST_REWARD
                
                # Create danger zone
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        danger_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
                        if danger_pos in self.grid and danger_pos not in self.walls:
                            manhattan_dist = abs(dx) + abs(dy)
                            self.grid[danger_pos] += self.GHOST_REWARD / (manhattan_dist + 1)

    def executeValueIteration(self, state):
        
        #Perform value iteration to calculate utilities for each state
        #using the Bellman equation: U(s) = R(s) + γ * max_a Σ P(s'|s,a) * U(s')
        # Initialize utilities for all grid positions to 0
        current_utilities = {pos: 0.0 for pos in self.grid}
        
        # Perform value iteration for specified number of iterations
        for _ in range(self.iteration_count):
            next_utilities = {}
            
            # Update utilities for each non-wall position
            for position in self.grid:
                if position in self.walls:
                    continue
                    
                # Find the action that maximizes expected utility
                action_utilities = []
                for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                    # Get possible outcomes and their probabilities for this action
                    state_transitions = self.getPossibleOutcomes(position, action)
                    
                    # Calculate expected utility for this action
                    expected_utility = sum(
                        probability * current_utilities.get(next_state, 0)
                        for next_state, probability in state_transitions
                    )
                    action_utilities.append(expected_utility)
                
                # Bellman equation: U(s) = R(s) + γ * max_a Σ P(s'|s,a) * U(s')
                next_utilities[position] = (
                    self.grid[position] + 
                    self.discount * max(action_utilities)
                )
            
            current_utilities = next_utilities
        
        self.utilities = current_utilities

    def getAction(self, state):
        """Choose the best action based on current state."""
        if self.first_move:
            self.initializeGameBoard(state)
            self.first_move = False

        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        current_pos = api.whereAmI(state)
        food = api.food(state)
        
        # Direct path to food if adjacent and safe
        for f in food:
            if self.calculateDistance(current_pos, f) == 1:
                is_safe = True
                for ghost_pos, is_scared in api.ghostStates(state):
                    if not is_scared:
                        ghost_x, ghost_y = int(ghost_pos[0]), int(ghost_pos[1])
                        if self.calculateDistance((ghost_x, ghost_y), f) <= 1:
                            is_safe = False
                            break
                
                if is_safe:
                    for action in legal:
                        next_pos = self.predictNextPosition(current_pos, action)
                        if next_pos == f:
                            return api.makeMove(action, legal)

        # Emergency ghost avoidance
        for ghost_pos, is_scared in api.ghostStates(state):
            if not is_scared:
                ghost_x, ghost_y = int(ghost_pos[0]), int(ghost_pos[1])
                ghost_dist = self.calculateDistance(current_pos, (ghost_x, ghost_y))
                
                if ghost_dist <= 2:
                    best_action = None
                    max_distance = -float('inf')
                    for action in legal:
                        next_pos = self.predictNextPosition(current_pos, action)
                        distance = self.calculateDistance(next_pos, (ghost_x, ghost_y))
                        if distance > max_distance:
                            max_distance = distance
                            best_action = action
                    if best_action:
                        return api.makeMove(best_action, legal)

        # Update rewards and run value iteration
        self.refreshGhostValues(state)
        self.executeValueIteration(state)

        # Choose best action based on utilities and food distances
        max_score = float('-inf')
        best_action = None

        for action in legal:
            next_pos = self.predictNextPosition(current_pos, action)
            # Calculate utility score
            successors = self.getPossibleOutcomes(current_pos, action)
            utility = sum(prob * self.utilities.get(next_pos, 0) for next_pos, prob in successors)
            
            # Add bonus for moving towards food
            min_food_dist = float('inf')
            for f in food:
                dist = self.calculateDistance(next_pos, f)
                min_food_dist = min(min_food_dist, dist)
            
            # Add small ghost safety factor
            ghost_safety = 0
            for ghost_pos, is_scared in api.ghostStates(state):
                if not is_scared:
                    ghost_x, ghost_y = int(ghost_pos[0]), int(ghost_pos[1])
                    dist = self.calculateDistance(next_pos, (ghost_x, ghost_y))
                    if dist < 2:
                        ghost_safety = -500
            
            # Combine utility with food distance bonus and ghost safety
            score = utility + (1.0 / (min_food_dist + 1)) * self.FOOD_REWARD + ghost_safety
            
            if score > max_score:
                max_score = score
                best_action = action

        return api.makeMove(best_action, legal)

    def final(self, state):
        """Reset state at the end of game"""
        self.utilities.clear()
        self.grid.clear()
        self.first_move = True
        self.previous_action = None