# analysis_h1.py
import random
import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents

def run_h1(daily_edges, num_days=120, num_runs=100):
    rng = random.Random(42)
    num_agents = estimate_num_agents(daily_edges)
    households = build_households(num_agents, household_size=4, rng=rng)

    final_individual = []
    final_household = []
    
    for _ in range(num_runs):
        seq = bootstrap_contact_sequence(daily_edges, num_days=num_days, rng=rng)

        # Scenario A: isolate symptomatic only
        simA = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.03,
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=True,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=0.001,
        )
        simA.seed_initial_infections(3)
        I_curve_A, final_R_A = simA.run(contact_reduction=1.0)
        final_individual.append(final_R_A)

        # Scenario B: isolate households too
        simB = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.03,
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=True,
            isolate_households=True,
            vaccination_coverage=0.0,
            external_infection_prob=0.001,
        )
        simB.seed_initial_infections(3)
        I_curve_B, final_R_B = simB.run(contact_reduction=1.0)
        final_household.append(final_R_B)

    final_individual = np.array(final_individual)
    final_household = np.array(final_household)

    mean_individual = final_individual.mean()
    mean_household = final_household.mean()
    reduction = 1 - (mean_household / mean_individual)

    print("H1:")
    print("  Mean total infections (individual isolation):", mean_individual)
    print("  Mean total infections (household isolation):", mean_household)
    print("  Relative reduction:", reduction)
    return reduction
