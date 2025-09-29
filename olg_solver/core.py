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
    """The economic environment, managing a population of general Agents."""
    def __init__(self, population, g):
        self.population = population
        self.g = g

    def get_aggregate_savings(self, R):
        """Calculates total net savings by asking each agent to solve its problem."""
        total_savings = 0
        for agent, share in self.population.items():
            solution = agent.solve(R, self.g)
            if solution is not None:
                total_savings += solution['savings'] * share
        return total_savings

class Solver:
    """Finds the equilibrium interest rate for a given Economy."""
    def __init__(self, economy):
        self.economy = economy

    def find_equilibrium_R(self, R_min=0.8, R_max=1.5):
        """Finds the market-clearing gross interest rate R*."""
        try:
            equilibrium_R = brentq(self.economy.get_aggregate_savings, a=R_min, b=R_max)
            return equilibrium_R
        except ValueError:
            print("Solver failed: The aggregate savings function does not have opposite signs at the bracket endpoints.")
            return None