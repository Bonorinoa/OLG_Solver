import numpy as np
import pandas as pd
from .core import Agent, Economy, Solver
from .components import Firm, Government

class ComparativeStatics:
    """
    An analysis engine to run comparative statics on various OLG model configurations.
    """
    def __init__(self, base_config):
        """
        Initializes the engine with a baseline model configuration.

        Args:
            base_config (dict): A dictionary containing all baseline parameters.
        """
        self.base_config = base_config

    def run(self, parameter_to_vary, values):
        """
        Runs a comparative statics experiment by varying one parameter.
        """
        results_list = []
        
        for value in values:
            # Create a mutable copy of the baseline config for this run
            current_config = self.base_config.copy()
            
            # Update the parameter being varied
            current_config[parameter_to_vary] = value
            
            # --- Build the model from the current configuration ---
            
            # Utility Function (handles changes in beta)
            beta = current_config['beta']
            utility_func = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)
            
            # Agent Population
            phi = current_config['phi']
            saver = Agent(utility_func, **current_config['endowments']['saver'])
            borrower = Agent(utility_func, **current_config['endowments']['borrower'])
            population = {saver: phi, borrower: 1 - phi}
            
            # Firm (optional)
            firm = Firm(**current_config['firm_params']) if 'firm_params' in current_config else None
            
            # Government (optional)
            gov = Government(**current_config['gov_params']) if 'gov_params' in current_config else None

            # --- Create and solve the economy ---
            economy = Economy(population, g=current_config['g'], firm=firm, government=gov)
            solver = Solver(economy)
            R_star = solver.find_equilibrium_R()
            
            results_list.append({
                'param_value': value,
                'R_star': R_star
            })
            
        return pd.DataFrame(results_list)