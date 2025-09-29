import numpy as np

# can be extended to any production function at the cost of efficiency
# for now, we assume a Cobb-Douglas production function and use known results to sidestep optimization

class Firm:
    """
    Represents a firm that maximizes profits by demanding capital and labor.
    Assumes a Cobb-Douglas production function: Y = A * K^alpha * L^(1-alpha).
    """
    def __init__(self, A, alpha, delta):
        """
        Initializes the Firm with its production technology.
        
        Args:
            A (float): Total Factor Productivity (TFP).
            alpha (float): The output elasticity of capital (capital's share).
            delta (float): The depreciation rate of capital.
        """
        self.A = A
        self.alpha = alpha
        self.delta = delta

    def solve(self, r, w):
        """
        Solves the firm's profit maximization problem given market prices.
        
        Args:
            r (float): The net real interest rate (cost of capital).
            w (float): The real wage (cost of labor).
            
        Returns:
            dict: A dictionary containing the firm's optimal choices.
        """
        # From the firm's FOC for capital: MPK = r + delta
        capital_labor_ratio = (self.A * self.alpha / (r + self.delta))**(1 / (1 - self.alpha))

        # We normalize total labor in the economy to 1 for simplicity
        L_d = 1.0
        K_d = capital_labor_ratio * L_d
        
        # Calculate total output and profits based on optimal choices
        output = self.A * (K_d**self.alpha) * (L_d**(1 - self.alpha))
        profit = output - (r + self.delta) * K_d - w * L_d
        
        return {
            "capital_demand": K_d,
            "labor_demand": L_d,
            "output": output,
            "profit": profit
        }
        
class Government:
    """
    Represents the government, which sets a complete fiscal policy.
    """
    def __init__(self, tax_rate_young=0.0, tax_rate_old=0.0, G=0.0, transfer_payment=0.0):
        """
        Initializes the Government with its policy parameters.

        Args:
            tax_rate_young (float): Tax rate on young's endowment.
            tax_rate_old (float): Tax rate on old's endowment.
            G (float): Government consumption (e.g., public goods).
            transfer_payment (float): Lump-sum transfer payment to agents.
        """
        self.tax_rate_young = tax_rate_young
        self.tax_rate_old = tax_rate_old
        self.G = G
        self.transfer_payment = transfer_payment