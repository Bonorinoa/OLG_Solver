import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.analysis import ComparativeStatics

# --- Define a Baseline Configuration for a Full Economy ---
# We use the same baseline as the final experiment to ensure comparability.
baseline_config = {
    "beta": 0.96, # This value will be overridden in the experiment
    "phi": 0.5,
    "g": 0.02,
    "endowments": {
        'saver': {'endowment_young': 10.0, 'endowment_old': 3.0},
        'borrower': {'endowment_young': 3.0, 'endowment_old': 10.0}
    },
    "firm_params": {
        "A": 1.0, 
        "alpha": 0.33,
        "delta": 0.05
    },
    "gov_params": { # We'll keep a neutral government for this experiment
        "tax_rate_young": 0.0,
        "tax_rate_old": 0.0,
        "G": 0.0,
        "transfer_payment": 0.0
    }
}

# --- Create the Analysis Engine ---
analysis_engine = ComparativeStatics(baseline_config)

# --- Run the Experiment: How does patience affect the interest rate? ---
print("Running Patience Experiment: Varying the discount factor (beta)...")

beta_values = np.linspace(0.90, 0.99, 15)

# The 'run' method in our analysis engine is perfect for this.
results_df = analysis_engine.run(parameter_to_vary='beta', values=beta_values)

# --- Plot the Results ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))
plt.plot(results_df['param_value'], results_df['R_star'], 'o-', color='crimson')
plt.title('Effect of Patience ($\\beta$) on the Interest Rate in a Production Economy', fontsize=14)
plt.xlabel('Time Discount Factor ($\\beta$)', fontsize=12)
plt.ylabel('Equilibrium Gross Interest Rate ($R^*$)', fontsize=12)
plt.savefig("beta_comparative_statics.png")
plt.show()

print("--- Analysis of Patience ---")
print(results_df)