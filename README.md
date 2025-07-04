# SMFD – Stochastic Modeling & Financial Derivatives

Welcome to the SMFD course repository. This project contains weekly Jupyter notebooks exploring topics in stochastic processes, SDEs, and financial derivatives, with both theoretical concepts and practical implementations.

---

Each week contains problems, derivations, and Python simulations. Week 5 includes an **interactive python notebook** to simulate Geometric Brownian Motion and price options.

---

## Week 5 Interactive Notebook: Euler–Maruyama Simulation

Features:
- Simulates Geometric Brownian Motion using the Euler–Maruyama method
- Prices:
  - European Call
  - Arithmetic Asian Call
  - Geometric Asian Call
  - Floating Lookback Call
- Interactive widgets to modify:
  - Spot price, drift, volatility
  - Strike, risk-free rate
  - Time horizon, time steps, and number of paths

---

## Launch the Interactive App (via Voilà + Binder)

Click below to run the interactive notebook live (no installation needed):

[![Launch on Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IdhantKadela/SMFD/HEAD?urlpath=voila/render/Week%205/Problem%20and%20Solution/Euler-Maruyama.ipynb)

---
## Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/IdhantKadela/SMFD.git
   cd SMFD/Week\ 5/Problem\ and\ Solution

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

3. Launch the Voilà web app:
   ```bash
   voila Euler-Maruyama.ipynb

---

## Authors
- **Idhant Kadela**
- **Aaditya Rathi**
- **Jatin Kawatra**

Course: Summer Project : Stochastic Modeling and Financial Derivatives, Stamatics, IIT Kanpur
