import numpy as np
from scipy.optimize import minimize, brentq

class Agent:
    """Represents a general agent who numerically solves their utility maximization problem."""
    def __init__(self, utility_func, endowment_young, endowment_old):
        self.utility_func = utility_func
        self.endowment_young = endowment_young
        self.endowment_old = endowment_old

    def solve(self, R, g):
        """Numerically solves the agent's utility maximization problem."""
        def objective(consumption):
            c_young, c_old = consumption
            return -self.utility_func(c_young, c_old)

        effective_old_endowment = self.endowment_old * (1 + g)
        def budget_constraint(consumption):
            c_young, c_old = consumption
            return self.endowment_young + (effective_old_endowment / R) - c_young - (c_old / R)

        constraints = ({'type': 'eq', 'fun': budget_constraint})
        initial_guess = [self.endowment_young / 2, effective_old_endowment / 2]
        solution = minimize(objective, initial_guess, constraints=constraints, tol=1e-9)

        if not solution.success:
            print(f"Warning: Optimizer failed for R={R}, g={g}")
            return None

        c_young_star, c_old_star = solution.x
        savings_star = self.endowment_young - c_young_star
        utility_star = self.utility_func(c_young_star, c_old_star)

        return {
            "c_young": c_young_star,
            "c_old": c_old_star,
            "savings": savings_star,
            "utility": utility_star
        }

class Economy:
    """The economic environment, managing agents and optionally a firm."""
    def __init__(self, population, g, firm=None):
        self.population = population
        self.g = g
        self.firm = firm # Can be None for a pure exchange economy

    def get_market_imbalance(self, R):
        """
        Calculates the imbalance in the capital market.
        This is the core function the Solver will target.
        """
        # 1. Calculate Aggregate Savings (Capital Supply from Agents)
        aggregate_savings = 0
        for agent, share in self.population.items():
            solution = agent.solve(R, self.g)
            if solution is not None:
                aggregate_savings += solution['savings'] * share
        
        # If there's no firm, the market clears when aggregate savings are zero
        if not self.firm:
            return aggregate_savings

        # --- If a firm exists, the market clears when S = I (or S = K_d) ---
        
        # 2. Determine Prices for the Firm
        r = R - 1 # Convert Gross R to net r for the firm's decision
        
        # With inelastic labor supply (L=1), the wage must equal the marginal product of labor
        # First, find the K/L ratio the firm desires at this interest rate 'r'
        k_l_ratio = (self.firm.A * self.firm.alpha / (r + self.firm.delta))**(1 / (1 - self.firm.alpha))
        
        # The equilibrium wage is the MPL at that K/L ratio
        w_eq = self.firm.A * (1 - self.firm.alpha) * (k_l_ratio**self.firm.alpha)

        # 3. Calculate the Firm's Capital Demand at these prices
        firm_solution = self.firm.solve(r, w_eq)
        capital_demand = firm_solution['capital_demand']

        # 4. Return the market imbalance: Supply - Demand
        return aggregate_savings - capital_demand

class Solver:
    """Finds the equilibrium interest rate for a given Economy."""
    def __init__(self, economy):
        self.economy = economy

    def find_equilibrium_R(self, R_min=1.01, R_max=1.5):
        """Finds the R that makes the market imbalance zero."""
        try:
            # Note: We now call the general 'get_market_imbalance' method
            equilibrium_R = brentq(self.economy.get_market_imbalance, a=R_min, b=R_max)
            return equilibrium_R
        except ValueError:
            print("Solver failed: The market imbalance function may not cross zero in the given bracket.")
            return None