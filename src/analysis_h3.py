import random
import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents

def run_h3(daily_edges, num_days=120, num_runs=300):
    rng = random.Random(999)
    num_agents = estimate_num_agents(daily_edges)
    households = build_households(num_agents, household_size=4, rng=rng)

    large_no_vax = []
    large_vax = []

    LARGE_OUTBREAK_THRESH = 0.5  # 50% infected

    for _ in range(num_runs):
        seq = bootstrap_contact_sequence(daily_edges, num_days=num_days, rng=rng)

        # --- No vaccination ---
        sim_no = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.09,      # a bit bigger to strengthen spread
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=0.001,
        )
        sim_no.seed_initial_infections(3)
        I_no, final_R_no = sim_no.run(contact_reduction=1.0)
        attack_no = final_R_no / num_agents
        large_no_vax.append(attack_no >= LARGE_OUTBREAK_THRESH)

        # --- 30% vaccination ---
        sim_vax = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.09,
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.30,
            external_infection_prob=0.001,
        )
        sim_vax.seed_initial_infections(3)
        I_vax, final_R_vax = sim_vax.run(contact_reduction=1.0)
        attack_vax = final_R_vax / num_agents
        large_vax.append(attack_vax >= LARGE_OUTBREAK_THRESH)

    large_no_vax = np.array(large_no_vax, dtype=bool)
    large_vax = np.array(large_vax, dtype=bool)

    p_no = large_no_vax.mean()
    p_vax = large_vax.mean()

    if p_no == 0:
        reduction_prob = float("nan")
    else:
        reduction_prob = 1 - (p_vax / p_no)

    print("H3:")
    print("  P(large outbreak) no vax:", p_no)
    print("  P(large outbreak) 30% vax:", p_vax)
    print("  Relative reduction:", reduction_prob)

    return p_no, p_vax, reduction_prob
