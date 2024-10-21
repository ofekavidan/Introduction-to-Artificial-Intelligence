<h1 align="center">Exercise 4 - Hanoi</h1>

## Project Overview

This project is part of the **Artificial Intelligence** course at HUJI (Hebrew University of Jerusalem). The goal of this exercise is to implement a **Planning Graph Algorithm** to solve various planning problems. This algorithm is commonly used in AI for solving tasks in domains such as the **Tower of Hanoi** and other classical planning problems. The project involves creating a graph-based representation of a problem's actions and states, which is used to determine a solution.

## Repository Structure

- **`action.py`**: Defines the actions used in planning problems.
- **`action_layer.py`**: Implements layers of actions within the planning graph, used to model the effects of actions at different levels of the graph.
- **`graph_plan.py`**: The main script that runs the Planning Graph algorithm for solving problems.
- **`hanoi.py`**: Implements the Tower of Hanoi problem as a planning problem.
- **`pgparser.py`**: Parses input files for planning problems.
- **`plan_graph_level.py`**: Represents the levels of the Planning Graph.
- **`planning_problem.py`**: Defines the structure of a planning problem, including states, goals, and actions.
- **`proposition.py`**: Defines propositions (logical statements) used in the planning problem.
- **`proposition_layer.py`**: Implements layers of propositions within the planning graph.
- **`search.py`**: Implements search algorithms used to traverse the Planning Graph and find a solution.

