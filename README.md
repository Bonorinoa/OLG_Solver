# OLG-Solver: A General Equilibrium Modeling Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular, object-oriented solver for steady-state Overlapping Generations (OLG) general equilibrium models in Python, implementing the Diamond (1965) model with production and government sectors.

## Overview

This project provides a flexible framework for building, solving, and analyzing OLG models from their economic primitives. Based on the seminal work of Samuelson (1958) and Diamond (1965), it enables users to construct economies where finite-lived agents interact through capital markets, creating rich intergenerational dynamics impossible in infinite-horizon models.

The system is designed for both **pedagogical use** (building economic intuition about lifecycle behavior, capital formation, and fiscal policy) and **research applications** (rapid prototyping of theoretical extensions and policy analysis).

### Architecture: "LEGO Brick" Philosophy

The framework consists of composable classes representing distinct economic actors:

- **`Agent`**: Consumers who numerically solve two-period utility maximization problems with heterogeneous endowment profiles
- **`Firm`**: Profit-maximizing producers with Cobb-Douglas technology that transform savings into productive capital
- **`Government`**: Fiscal authority implementing tax, transfer, and spending policies with automatic budget balancing
- **`Economy`**: Market coordinator that aggregates agent behavior and enforces general equilibrium conditions  
- **`Solver`**: Root-finding engine that computes market-clearing interest rates using numerical methods
- **`ComparativeStatics`**: Automated analysis engine for systematic parameter sensitivity studies

## Key Features

- **Solve Models from Economic Primitives:** Define agent preferences with arbitrary Python utility functions—no analytical derivations required
- **Modular Architecture:** Build economies of varying complexity by selecting components (pure exchange, production, government sectors)
- **Numerical Robustness:** Uses scipy optimization for agent problems and root-finding for market clearing with automatic convergence handling
- **Rich Policy Analysis:** Built-in government sector supports complex fiscal experiments (taxation, transfers, public spending)
- **Automated Comparative Statics:** Systematic parameter variation analysis with publication-ready visualizations
- **Heterogeneous Agents:** Support for multiple agent types with different endowment profiles and population shares
- **Research Extensions:** Clean API enables easy incorporation of new features (alternative utility functions, production technologies, policy instruments)

## Theoretical Foundation

The solver implements **Diamond's (1965) OLG model with production**, extending Samuelson's (1958) pure exchange framework. Key theoretical elements:

- **Finite Lifespans:** Agents live exactly two periods (young/old), creating realistic lifecycle saving behavior
- **Overlapping Cohorts:** Multiple generations coexist, enabling intergenerational transfers through capital markets
- **Dynamic Efficiency:** Unlike Ramsey models, OLG economies can exhibit dynamic inefficiency where excessive saving reduces welfare
- **Endogenous Interest Rates:** Capital returns determined by marginal productivity and agent intertemporal preferences
- **Fiscal Policy Effects:** Government actions directly affect private saving decisions and long-run capital formation

## Model Assumptions

The implementation makes several standard assumptions consistent with Diamond (1965):

- **Two-Period Lives:** Agents work when young, consume savings when old (no early death uncertainty)
- **Cobb-Douglas Production:** Firms use Y = A·K^α·L^(1-α) with constant returns to scale
- **Perfect Competition:** All agents are price-takers in competitive markets
- **Inelastic Labor Supply:** Each young agent supplies exactly one unit of labor
- **Perfect Capital Depreciation:** Capital stock fully depreciates each period (δ = 100% implicitly)
- **Perfect Foresight:** Agents have complete information about future prices and policies
- **Balanced Government Budget:** Tax revenues equal government spending plus transfers each period

## Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bonorinoa/OLG_Solver.git
   cd OLG_Solver
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv olg_venv
   source olg_venv/bin/activate  # On Windows: olg_venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run example analyses:**
   
   **Basic exchange economy:**
   ```bash
   python scripts/01_run_basic_model.py
   ```
   
   **Production economy with firms:**
   ```bash
   python scripts/03_run_production_model.py  
   ```
   
   **Full system with fiscal policy:**
   ```bash
   python scripts/04_run_full_system.py
   ```

4. **Explore comparative statics:**
   ```bash
   python scripts/02_run_comparative_statics.py
   ```

## Project Structure

```
OLG_Solver/
├── olg_solver/              # Core package
│   ├── core.py             # Agent, Economy, Solver classes
│   ├── components.py       # Firm and Government classes  
│   └── analysis.py         # ComparativeStatics engine
├── scripts/                # Example applications
│   ├── 01_run_basic_model.py      # Pure exchange economy
│   ├── 02_run_comparative_statics.py  # Parameter sensitivity
│   ├── 03_run_production_model.py     # Economy with firms
│   └── 04_run_full_system.py         # Complete system + government
├── requirements.txt        # Dependencies (pandas, numpy, scipy, matplotlib)
└── README.md              # This file
```

## Example Applications

### Pure Exchange Economy
Study how heterogeneous agents (savers vs. borrowers) trade through financial markets:
- Agents with different endowment profiles across life stages
- Market-clearing interest rates balance saving and borrowing desires
- No production sector—purely redistributive financial system

### Production Economy  
Analyze how savings translate into productive investment:
- Firms demand capital for production using Cobb-Douglas technology
- Interest rates reflect marginal productivity of capital
- Demonstrates classical growth theory mechanisms

### Fiscal Policy Analysis
Examine government interventions in OLG settings:
- Tax effects on private saving incentives and capital formation
- Transfer programs and intergenerational redistribution
- Dynamic inefficiency and potential for welfare-improving policy

### Comparative Statics
Systematic exploration of parameter effects:
- Population composition (share of saver vs. borrower types)  
- Technological parameters (productivity, capital share)
- Policy parameters (tax rates, government spending)
- Preference parameters (time discount factor, risk aversion)

## Quick Usage Example

```python
import numpy as np
from olg_solver.core import Agent, Economy, Solver
from olg_solver.components import Firm, Government

# Define log utility with time preference
beta = 0.96
utility = lambda c_y, c_o: np.log(c_y) + beta * np.log(c_o)

# Create heterogeneous agents
saver = Agent(utility, endowment_young=10.0, endowment_old=3.0)
borrower = Agent(utility, endowment_young=3.0, endowment_old=10.0)
population = {saver: 0.6, borrower: 0.4}  # 60% savers, 40% borrowers

# Add production sector
firm = Firm(A=1.0, alpha=0.33, delta=0.05)  # TFP, capital share, depreciation

# Add government sector  
gov = Government(tax_rate_young=0.1, transfer_payment=0.5)

# Solve for equilibrium
economy = Economy(population, g=0.02, firm=firm, government=gov)
solver = Solver(economy)
R_star = solver.find_equilibrium_R()

print(f"Equilibrium gross interest rate: {R_star:.4f}")
```

## Key Economic Insights

### Why OLG Models Matter
Unlike infinite-horizon models (Ramsey-Cass-Koopmans), OLG models capture crucial features of real economies:

1. **Finite Lifespans:** Realistic lifecycle saving patterns with working and retirement phases
2. **Intergenerational Transfers:** Capital markets facilitate transfers from young savers to old dissavers
3. **Dynamic Inefficiency:** Economies can oversave, creating welfare-improving roles for government policy
4. **Fiscal Policy Relevance:** Government interventions have permanent effects on long-run capital formation

### Model Predictions
- **Interest Rates:** Determined by intersection of private saving supply and investment demand
- **Capital Formation:** Higher saving rates increase steady-state capital stock and output
- **Fiscal Policy:** Taxes on young reduce private saving; transfers to old reduce saving incentives  
- **Population Effects:** More savers → higher capital stock; more borrowers → lower capital stock

## Research Extensions

The modular design facilitates research extensions:

- **Alternative Utility Functions:** Replace log utility with CRRA, Epstein-Zin, or other specifications
- **Endogenous Labor Supply:** Modify agents to choose optimal work hours
- **Stochastic Models:** Add uncertainty to endowments, productivity, or lifespans
- **Multi-Sector Production:** Extend to consumption and investment goods sectors
- **Social Security:** Implement PAYG pension systems with endogenous retirement decisions
- **Human Capital:** Add education investment decisions and skill accumulation
- **International Trade:** Multi-country versions with capital mobility

## Dependencies

- **Python 3.7+**
- **NumPy:** Array operations and mathematical functions
- **SciPy:** Numerical optimization (agent problems) and root-finding (equilibrium)  
- **Pandas:** Data manipulation for comparative statics results
- **Matplotlib:** Visualization of equilibrium outcomes and policy effects

## Citation

If you use this code in your research, please cite:

```bibtex
@software{olg_solver_2025,
  title = {OLG-Solver: A General Equilibrium Modeling Toolkit},
  authors = {Augusto Gonzalez-Bonorino, Gemini 2.5 Pro},
  year = {2025},
  url = {https://github.com/Bonorinoa/OLG_Solver}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests for:
- Bug fixes and performance improvements
- Additional example applications  
- New economic features or extensions
- Documentation improvements
- Test coverage expansion

## References

- Diamond, P. A. (1965). "National debt in a neoclassical growth model." *American Economic Review*, 55(5), 1126-1150.
- Samuelson, P. A. (1958). "An exact consumption-loan model of interest with or without the social contrivance of money." *Journal of Political Economy*, 66(6), 467-482.
- Galor, O. (1992). "A two-sector overlapping-generations model: A global characterization of the dynamical system." *Econometrica*, 60(6), 1351-1386.