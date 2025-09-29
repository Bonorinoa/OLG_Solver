import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.core import Agent, Economy, Solver

# --- Baseline Setup ---
# Define the components that will be common across most experiments
beta = 0.96
log_utility = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)

saver_agent = Agent(
    utility_func=log_utility,
    endowment_young=10.0,
    endowment_old=3.0
)
borrower_agent = Agent(
    utility_func=log_utility,
    endowment_young=3.0,
    endowment_old=10.0
)

# --- Experiment 1: The Effect of Population Composition (phi) ---

print("Running Experiment 1: Varying phi...")
phi_values = np.linspace(0.1, 0.9, 20)
results_phi = []

for phi in phi_values:
    # Re-create the population and economy for each value of phi
    population = {saver_agent: phi, borrower_agent: 1 - phi}
    economy = Economy(population=population, g=0.02)
    solver = Solver(economy)
    
    R_star = solver.find_equilibrium_R(R_min=0.5, R_max=4.0)
    if R_star is not None:
        results_phi.append(R_star)
    else:
        results_phi.append(np.nan) # Append NaN if solver fails

# Plotting the results for Experiment 1
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))
plt.plot(phi_values, results_phi, 'o-')
plt.title('Effect of Population Composition ($\phi$) on the Interest Rate', fontsize=16)
plt.xlabel('Fraction of Savers in the Population ($\phi$)', fontsize=12)
plt.ylabel('Equilibrium Gross Interest Rate ($R^*$)', fontsize=12)
plt.savefig("phi_comparative_statics.png") # Save the figure
plt.show()

# --- Experiment 2: The Effect of Technological Growth (g) ---

print("Running Experiment 2: Varying g...")
g_values = np.linspace(0.0, 0.05, 20)
results_g = []

# For this experiment, phi is fixed
phi = 0.5
population = {saver_agent: phi, borrower_agent: 1 - phi}

for g_rate in g_values:
    # Re-create the economy for each value of g
    economy = Economy(population=population, g=g_rate)
    solver = Solver(economy)

    R_star = solver.find_equilibrium_R(R_min=0.8, R_max=1.5)
    if R_star is not None:
        results_g.append(R_star)
    else:
        results_g.append(np.nan)

# Plotting the results for Experiment 2
plt.figure(figsize=(10, 6))
plt.plot(g_values, results_g, 's-', color='green')
plt.title('Effect of Tech Growth (g) on the Interest Rate', fontsize=16)
plt.xlabel('Technological Growth Rate (g)', fontsize=12)
plt.ylabel('Equilibrium Gross Interest Rate ($R^*$)', fontsize=12)
plt.savefig("g_comparative_statics.png") # Save the figure
plt.show()

print("Comparative statics analysis complete.")