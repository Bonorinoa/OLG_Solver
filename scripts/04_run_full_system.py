import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.analysis import ComparativeStatics

# --- Define a Baseline Configuration for a Full Economy ---
# This dictionary is the "master input" for our analysis engine.
baseline_full_economy = {
    "beta": 0.96,
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
    "gov_params": {
        "tax_rate_young": 0.2, # Baseline 10% tax on the young
        "tax_rate_old": 0.0,
        "G": 0.0, # All tax revenue is for pensions (transfer_payment)
        "transfer_payment": 0.0 # This will be calculated by the Economy
    }
}

# --- Create the Analysis Engine ---
analysis_engine = ComparativeStatics(baseline_full_economy)

# --- Run the Experiment: How do taxes affect the interest rate? ---
print("Running Final Experiment: Varying the tax rate on the young...")

# We will vary the 'tax_rate_young' within the 'gov_params' dictionary.
# This requires a slightly more advanced loop than the class provides,
# but showcases the system's flexibility.

tax_rates = np.linspace(0.0, 0.4, 15) # From 0% to 40%
results = []

for tax in tax_rates:
    # Create a copy of the config and update the tax rate
    config = baseline_full_economy.copy()
    config['gov_params']['tax_rate_young'] = tax
    
    # Re-initialize the engine with the new config for this single run
    engine = ComparativeStatics(config)
    # The 'run' method is simple here, as we only need one data point
    df = engine.run('g', [config['g']]) # Vary 'g' over a single value to get R*
    
    results.append({
        'tax_rate': tax,
        'R_star': df['R_star'].iloc[0]
    })

import pandas as pd
results_df = pd.DataFrame(results)

# --- Plot the Final Results ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))
plt.plot(results_df['tax_rate'], results_df['R_star'], 'o-', color='purple')
plt.title('Effect of a Youth Tax on the Interest Rate in a Production Economy', fontsize=14)
plt.xlabel('Tax Rate on Young Agent\'s Endowment', fontsize=12)
plt.ylabel('Equilibrium Gross Interest Rate ($R^*$)', fontsize=12)
plt.savefig("final_experiment_tax_effect.png")
plt.show()

print("--- Analysis of a PAYG Pension System ---")
print(results_df)

# --- Economic Interpretation: Crowding Out Investment ---
"""
Taxes Reduce Savings: The tax on the young directly reduces their disposable income. 
For any given interest rate, both the "saver" and "borrower" types of agents have 
less money available. This leads to a decrease in their ability to save (or an 
increase in their need to borrow), which ultimately reduces the total supply of 
private savings available in the economy.

Less Capital for Firms: This decline in the supply of private savings means there 
are fewer funds available for the firm to borrow for investment. With a smaller 
pool of available capital, the firm invests less, leading to a smaller steady-state 
capital stock (K).

Diminishing Returns: According to the firm's production function, the marginal 
product of capital (MPK) is subject to diminishing returns. When the capital stock 
is high, the return on one extra unit of capital is low. Conversely, when the 
capital stock is low (as it is when taxes are high), the return on an additional 
unit of capital is high.

The Price Must Adjust: Since the equilibrium interest rate (r*) must equal the net 
marginal product of capital (MPK - δ), a lower capital stock implies a higher MPK 
and therefore a higher equilibrium interest rate. Conversely, lower taxes lead to 
more savings, a larger capital stock, a lower MPK, and thus a lower equilibrium 
interest rate.
"""