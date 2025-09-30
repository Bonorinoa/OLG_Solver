import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.core import Agent, Economy, Solver

# --- Experiment Setup ---

def run_tax_experiment(sigma, beta, ax):
    """Runs the comparative statics for a given sigma and plots on the given axes."""
    
    # Define the CRRA utility function for this experiment
    if sigma == 1.0:
        utility_func = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)
    else:
        utility_func = lambda c_y, c_o: (c_y**(1-sigma))/(1-sigma) + beta * (c_o**(1-sigma))/(1-sigma)

    # Agent Population (remains the same)
    saver = Agent(utility_func, endowment_young=10.0, endowment_old=3.0)
    borrower = Agent(utility_func, endowment_young=3.0, endowment_old=10.0)
    population = {saver: 0.5, borrower: 0.5}

    # Firm (remains the same)
    from olg_solver.components import Firm
    firm = Firm(A=1.0, alpha=0.33, delta=0.05)
    
    # Government
    from olg_solver.components import Government

    tax_rates = np.linspace(0.0, 0.4, 15)
    results = []

    print(f"\n--- Running for sigma = {sigma} (IES = {1/sigma:.2f}) ---")
    for tax in tax_rates:
        gov = Government(tax_rate_young=tax)
        economy = Economy(population, g=0.02, firm=firm, government=gov)
        solver = Solver(economy)
        R_star = solver.find_equilibrium_R(R_min=1.01, R_max=2.0)
        results.append({'tax_rate': tax, 'R_star': R_star})
        
    results_df = pd.DataFrame(results)
    
    # Plotting
    ies_label = f'IES = {1/sigma:.2f} ($\\sigma$={sigma})'
    ax.plot(results_df['tax_rate'], results_df['R_star'], 'o-', label=ies_label)
    
    return results_df

# --- Main Execution ---
fig, ax = plt.subplots(figsize=(12, 7))
plt.style.use('seaborn-v0_8-whitegrid')

# Run for flexible agents (high IES)
run_tax_experiment(sigma=0.5, beta=0.96, ax=ax)

# Run for rigid agents (low IES)
run_tax_experiment(sigma=4.0, beta=0.96, ax=ax)

# Final plot formatting
ax.set_title('Interest Rate Response to Taxes Depends on Intertemporal Elasticity', fontsize=16)
ax.set_xlabel("Tax Rate on Young Agent's Endowment", fontsize=12)
ax.set_ylabel("Equilibrium Gross Interest Rate ($R^*$)", fontsize=12)
ax.legend(title="Agent Preference Type", fontsize=11)
plt.savefig("ies_experiment.png")
plt.show()