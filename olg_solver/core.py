import numpy as np
from scipy.optimize import minimize, brentq
from .components import Government

class Agent:
    """Represents a general agent who numerically solves their utility maximization problem."""
    def __init__(self, utility_func, endowment_young, endowment_old):
        self.utility_func = utility_func
        self.endowment_young = endowment_young
        self.endowment_old = endowment_old

    def solve(self, R, g, government):
        """Numerically solves the agent's problem, now aware of government policy."""
        def objective(consumption):
            c_young, c_old = consumption
            return -self.utility_func(c_young, c_old)

        def budget_constraint(consumption):
            c_young, c_old = consumption
            # Net income when young (after tax)
            net_income_young = self.endowment_young * (1 - government.tax_rate_young)
            # Net income when old (after tax, plus any transfers)
            net_income_old = (self.endowment_old * (1 - government.tax_rate_old)) + government.transfer_payment
            
            pdv_resources = net_income_young + (net_income_old * (1 + g)) / R
            pdv_consumption = c_young + c_old / R
            return pdv_resources - pdv_consumption

        constraints = ({'type': 'eq', 'fun': budget_constraint})
        initial_guess = [self.endowment_young / 2, self.endowment_old / 2]
        solution = minimize(objective, initial_guess, constraints=constraints, tol=1e-9)

        if not solution.success:
            return None

        c_young_star, c_old_star = solution.x
        # Savings is now based on net income
        savings_star = (self.endowment_young * (1 - government.tax_rate_young)) - c_young_star
        utility_star = self.utility_func(c_young_star, c_old_star)
        
        return {"c_young": c_young_star, "c_old": c_old_star, "savings": savings_star, "utility": utility_star}


class Economy:
    """The economic environment, managing all agents and institutions."""
    def __init__(self, population, g, firm=None, government=None):
        self.population = population
        self.g = g
        self.firm = firm
        # If no government is provided, create a default one with no policies
        self.government = government if government is not None else Government()

    def get_market_imbalance(self, R):
        """Calculates the imbalance in the capital market: National Savings - Investment."""
        private_savings = 0
        total_young_endowment = 0
        total_old_endowment = 0
        
        for agent, share in self.population.items():
            solution = agent.solve(R, self.g, self.government)
            if solution is not None:
                private_savings += solution['savings'] * share
                total_young_endowment += agent.endowment_young * share
                total_old_endowment += agent.endowment_old * share

        # If there is no firm, investment is zero.
        investment = 0
        total_output = total_young_endowment + total_old_endowment # In exchange economy
        
        if self.firm:
            r = R - 1
            # For simplicity, assume wage adjusts to clear labor market (L=1)
            k_l_ratio = (self.firm.A * self.firm.alpha / (r + self.firm.delta))**(1 / (1 - self.firm.alpha))
            w_eq = self.firm.A * (1 - self.firm.alpha) * (k_l_ratio**self.firm.alpha)
            firm_solution = self.firm.solve(r, w_eq)
            investment = firm_solution['capital_demand']
            total_output = firm_solution['output']
        
        # Calculate Public Savings (S_public = T - G - Transfers)
        tax_rev_young = self.government.tax_rate_young * total_young_endowment
        tax_rev_old = self.government.tax_rate_old * total_old_endowment
        total_tax_revenue = tax_rev_young + tax_rev_old
        
        public_savings = total_tax_revenue - self.government.G - self.government.transfer_payment

        # National Savings = Private Savings + Public Savings
        national_savings = private_savings + public_savings

        return national_savings - investment

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