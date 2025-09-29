import sys
import os
import numpy as np

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.core import Agent, Economy, Solver

# 1. Define the utility function
beta = 0.96
log_utility = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)

# 2. Create the agents
saver = Agent(log_utility, endowment_young=10.0, endowment_old=3.0)
borrower = Agent(log_utility, endowment_young=3.0, endowment_old=10.0)

# 3. Define the economy
phi = 0.5
population = {saver: phi, borrower: 1 - phi}
economy = Economy(population=population, g=0.02)

# 4. Create the solver and find the equilibrium
solver = Solver(economy)
R_star = solver.find_equilibrium_R()

if R_star is not None:
    print("--- Basic Model Equilibrium Found! ---")
    print(f"The equilibrium gross interest rate R* is: {R_star:.4f}")
    # Verification
    imbalance = economy.get_aggregate_savings(R_star)
    print(f"Verification: Aggregate savings at R* are: {imbalance:.10f}")