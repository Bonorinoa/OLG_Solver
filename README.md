# OLG_Solver
A minimal OOP implementation of an Overlapping Generations General Equilibrium model. It supports three types of agents (consumer, firm, government) defined by their optimization problem. So each agent is characterized by an optimization problem, adhering to the single responsibility principle.  

## Overview

This project provides a flexible framework for building, solving, and analyzing OLG models. The core design is built on three components:
- **`Agent`**: A class that numerically solves an individual's utility maximization problem.
- **`Economy`**: A class that defines the economic environment, including the population of agents and global parameters.
- **`Solver`**: A class that finds the market-clearing interest rate for a given economy.

## Quickstart

To run a basic simulation:
1. Clone this repository.
2. Navigate to the root directory.
3. Run the example script:
   ```sh
   python scripts/01_run_basic_model.py