# Operational Research Project – Investigação Operacional I

This repository contains the coursework developed for the **Investigação Operacional I** class.  
It includes a full report in PDF and a Python implementation using Gurobi for solving facility location and vehicle allocation optimization problems.

## Project Goal
The main objective of this project was to **design and implement optimization models for locating emergency vehicles** in order to:
- Minimize the **total travel distance** from fire ignition points to the nearest vehicle,  
- Minimize the **maximum distance** any ignition point has to travel to reach a vehicle, and  
- Maximize the **coverage of high-risk ignition areas** (locations with higher fire risk) within a given distance threshold.  

These models simulate decision-making scenarios in emergency response planning, helping to optimize resource allocation in situations such as wildfire prevention and response.

## Contents
- `Relatório Trabalho Investigação Operacional I.pdf` – detailed report explaining the mathematical models, decision variables, constraints, objectives, and analysis of results.  
- `Trabalho Investigação Operacional I.py` – Python script implementing the optimization models using **Gurobi**, including visualization of solutions.  

## Technologies
- Python 3  
- [Gurobi Optimizer](https://www.gurobi.com/) (`gurobipy`)  
- `matplotlib`, `networkx` (for visualization)

