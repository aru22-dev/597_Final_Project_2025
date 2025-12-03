# Simulating Infectious Disease Spread in a Remote Village Using Monte Carlo Methods

## Overview
This project simulates the spread of a contagious disease within the context of a small, closely connected rural village using real‑world proximity data collected in Malawi. The goal is to understand how different intervention strategies influence outbreak severity when healthcare access is limited and the social contact network is dense.

The model leverages real timestamped proximity logs among 86 individuals to capture authentic daily contact patterns. Disease dynamics (transmission, incubation, infectious duration, symptoms) are modeled probabilistically to reflect real‑world biological uncertainty. The simulation is repeated under varied conditions using Monte Carlo techniques to observe the distribution of outcomes and evaluate non‑obvious patterns.

---

## Project Type
**Type II – Original Monte Carlo Simulation**

---

## Hypotheses
This project evaluates the impact of different interventions using repeated Monte Carlo trials:

1. **Household Quarantine** —  
   Isolating the entire household of a symptomatic individual reduces overall infections by **≥ 30%** compared to isolating only the symptomatic person.

2. **Contact Rate Reduction** —  
   Reducing the average contact rate from ~6 to ~3 contacts per day delays the outbreak peak by **≥ 5 days** and reduces peak caseload by **≥ 40%**.

3. **Pre‑emptive Vaccination** —  
   Vaccinating **30%** of the population before the outbreak will reduce the probability of a major outbreak (>50% infected) by **≥ 60%**.

Each hypothesis will be tested via controlled Monte Carlo experiments by modifying model parameters and analyzing the aggregate outputs.

---

## Simulation Design

### Core Concepts
- **Agents:** Each individual is modeled as an agent with states (Susceptible → Exposed → Infectious → Recovered).
- **Contact Network:** Contacts between individuals are derived directly from empirical proximity logs rather than synthetic assumptions.
- **Monte Carlo Runs:** Each scenario is simulated repeatedly (hundreds of independent trials) under randomized disease‑progression variables.
- **Interventions:**  
  - Household versus individual isolation  
  - Reducing contact rates  
  - Pre‑emptive vaccination  

### Random Variables
| Variable | Distribution | Notes |
|----------|--------------|-------|
| Incubation period | Log‑Normal | Mean ≈ 5.5 days |
| Infectious period | Gamma or Normal | Mean ≈ 7 days |
| Transmission probability | Beta(2,5) | Skewed, allows variability |
| Asymptomatic probability | Bernoulli(p=0.3) | ~30% asymptomatic |

These well‑chosen distributions reflect realistic epidemiological patterns and introduce stochasticity that allows non‑obvious outcomes to emerge across trials.

---

## Data Source
This project uses real proximity data from wearable sensors deployed in rural Malawi:

> **SocioPatterns: Contact Patterns in a Village in Rural Malawi**  
> http://www.sociopatterns.org/datasets/contact-patterns-in-a-village-in-rural-malawi/

These logs contain:
- Person‑to‑person contact pairs (`id1`, `id2`)
- Day index
- Timestamp of contact occurrence

The data form a time‑varying interaction network across several days.

### Primary Publication
Fournet & Barrat (2021)  
*Using wearable proximity sensors to characterize social contact patterns in a village of rural Malawi*  
https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00302-w

This publication describes data collection methodology and serves as the contextual foundation for model structure.

---

## Repository Structure
├── data/
│ └── malawi_contact_data.csv # Cleaned contact dataset
├── src/
│ ├── simulate.py # Main MC simulation
│ ├── agent.py # Person agent logic
│ ├── parameters.py # Disease parameters & distributions
│ └── experiments.py # Intervention setup
├── notebooks/
│ └── analysis.ipynb # Exploration + visualization
├── results/
│ └── (output CSVs / plots)
├── README.md
└── requirements.txt


> *Note: directory contents are placeholders and will be updated during development.*

---

## Requirements
- Python 3.8+
- NumPy
- Pandas
- Matplotlib / Seaborn
- (Optional) NetworkX
- Jupyter Notebook


Author

Arundhati Raj
GitHub: https://github.com/aru22-dev

Course: IS597PR — Fall 2025
Instructor: John Weible
