import sys
import os
import numpy as np

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from olg_solver.core import Agent, Economy, Solver
from olg_solver.components import Firm

# --- Setup the Economy's Components ---

# 1. Define the utility function for the agents
beta = 0.96
log_utility = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)

# 2. Create the agent population (savers and borrowers)
saver = Agent(log_utility, endowment_young=10.0, endowment_old=3.0)
borrower = Agent(log_utility, endowment_young=3.0, endowment_old=10.0)
population = {saver: 0.5, borrower: 0.5}

# 3. Create the firm with its production technology
#    A=1.0 (TFP), alpha=0.33 (capital share), delta=0.05 (depreciation)
production_firm = Firm(A=1.0, alpha=0.33, delta=0.05)

# --- Build and Solve the Economy ---

# 4. Create an instance of the Economy, now including the firm
economy_with_production = Economy(
    population=population,
    g=0.02,
    firm=production_firm  # <-- The key addition!
)

# 5. Create the solver and find the equilibrium interest rate
solver = Solver(economy_with_production)
# We might need a slightly wider bracket to find the new equilibrium
R_star = solver.find_equilibrium_R(R_min=0.5, R_max=2.0)

# --- Display the Results ---

if R_star is not None:
    print("--- Production Economy Equilibrium Found! ---")
    print(f"The equilibrium gross interest rate R* is: {R_star:.4f}")
    print(f"(This corresponds to a net interest rate r* of: {(R_star - 1)*100:.2f}%)")
    
    # Verification step
    imbalance = economy_with_production.get_market_imbalance(R_star)
    print(f"Verification: Capital market imbalance (Savings - K_demand) is: {imbalance:.10f}")

else:
    print("The solver could not find an equilibrium for the production economy.")

# --- Economic Analysis: From Pure Exchange to Production Economy ---
"""
In our old pure exchange economy, the interest rate was just a price that balanced 
the desires of some people to save with the desires of others to borrow. It was a 
closed loop, and the equilibrium r* was relatively low because there was nothing 
particularly productive to do with the savings. In an economy with production, the 
long-run interest rate is determined not just by people's patience (beta) but by 
the underlying productivity of capital.

By adding the Firm, we ripped that closed loop open. We introduced a powerful new 
force: a productive investment opportunity.

New Demand for Savings: The firm enters the market as a massive new borrower. It 
doesn't borrow to smooth its consumption; it borrows to buy capital (K) and generate 
real output. This creates a huge new demand for the economy's savings.

The Price Must Rise: To meet this new, hungry demand for investment funds, the 
households in the economy must be convinced to save a lot more than they did before. 
The only way to incentivize this massive increase in savings is for the price of 
savings—the interest rate—to skyrocket.

Driven by Productivity: The equilibrium interest rate is now fundamentally tied to 
the marginal product of capital (MPK). The parameters we gave the firm (A=1.0, 
alpha=0.33) describe a very productive technology. The firm is willing to pay a 
very high interest rate because the return it gets from investing in an additional 
unit of capital is also very high. The equilibrium r* of 36.61% reflects a world 
where the marginal return on investment is incredibly strong.
"""

