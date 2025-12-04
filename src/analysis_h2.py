import random
import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents

def run_h2(daily_edges, num_days=120, num_runs=200):
    rng = random.Random(123)
    num_agents = estimate_num_agents(daily_edges)
    households = build_households(num_agents, household_size=4, rng=rng)

    peak_day_high = []
    peak_I_high = []
    peak_day_low = []
    peak_I_low = []

    # Only count runs where we actually get a decent outbreak
    MIN_ATTACK = 0.2  # require at least 20% infected to treat as "real outbreak"

    for _ in range(num_runs):
        seq = bootstrap_contact_sequence(daily_edges, num_days=num_days, rng=rng)

        # --- High contacts (baseline) ---
        sim_high = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.08,        # slightly higher than 0.03 to get clearer outbreaks
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=0.001,
        )
        sim_high.seed_initial_infections(3)
        I_high, final_R_high = sim_high.run(contact_reduction=1.0)
        attack_high = final_R_high / num_agents

        # --- Low contacts (half or less) ---
        sim_low = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=0.08,
            infectious_days=5,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=0.001,
        )
        sim_low.seed_initial_infections(3)
        # Stronger reduction than before (try 0.4 or 0.3)
        I_low, final_R_low = sim_low.run(contact_reduction=0.4)
        attack_low = final_R_low / num_agents

        # Only keep runs where both scenarios had real outbreaks
        if attack_high >= MIN_ATTACK and attack_low >= MIN_ATTACK:
            peak_I_val_high = I_high.max()
            peak_I_high.append(peak_I_val_high)
            peak_day_high.append(int(I_high.argmax()))

            peak_I_val_low = I_low.max()
            peak_I_low.append(peak_I_val_low)
            peak_day_low.append(int(I_low.argmax()))

    peak_day_high = np.array(peak_day_high)
    peak_I_high = np.array(peak_I_high)
    peak_day_low = np.array(peak_day_low)
    peak_I_low = np.array(peak_I_low)

    mean_peak_day_high = peak_day_high.mean()
    mean_peak_day_low = peak_day_low.mean()
    mean_peak_I_high = peak_I_high.mean()
    mean_peak_I_low = peak_I_low.mean()

    delay = mean_peak_day_low - mean_peak_day_high
    reduction_peak = 1 - (mean_peak_I_low / mean_peak_I_high)

    print("H2:")
    print("  Mean peak day (high contacts):", mean_peak_day_high)
    print("  Mean peak day (low contacts):", mean_peak_day_low)
    print("  Delay (days):", delay)
    print("  Mean peak I (high):", mean_peak_I_high)
    print("  Mean peak I (low):", mean_peak_I_low)
    print("  Relative reduction in peak load:", reduction_peak)

    return delay, reduction_peak
