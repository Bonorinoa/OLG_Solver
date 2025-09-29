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
        
        The firm hires capital and labor such that their marginal products
        equal their respective prices.
        
        Args:
            r (float): The net real interest rate (cost of capital).
            w (float): The real wage (cost of labor).
            
        Returns:
            dict: A dictionary containing the firm's optimal choices.
        """
        # From the firm's FOC for capital: MPK = r + delta
        # A*alpha*(L/K)^(1-alpha) = r + delta
        # => (K/L) = (A*alpha / (r + delta))^(1/(1-alpha))
        capital_labor_ratio = (self.A * self.alpha / (r + self.delta))**(1 / (1 - self.alpha))

        # From the firm's FOC for labor: MPL = w
        # A*(1-alpha)*(K/L)^alpha = w
        # This gives us a second way to find the K/L ratio, which we can use
        # to ensure consistency or solve for other variables if needed.
        # For simplicity, we assume labor supply is inelastic (e.g., L=1)
        # for calculating total quantities. Let's normalize labor demand to 1.
        
        L_d = 1.0  # Normalize labor demand for simplicity
        K_d = capital_labor_ratio * L_d
        
        # Calculate total output
        output = self.A * (K_d**self.alpha) * (L_d**(1 - self.alpha))
        
        # Calculate total profits
        profits = output - (r + self.delta) * K_d - w * L_d
        
        return {
            "capital_demand": K_d,
            "labor_demand": L_d,
            "output": output,
            "profit": profits
        }