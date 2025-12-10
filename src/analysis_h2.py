import random
from typing import Dict, List, Tuple

import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents


def run_h2(
    daily_edges: Dict[int, List[Tuple[int, int]]],
    num_days: int = 120,
    num_runs: int = 200,
    infection_prob: float = 0.08,
    infectious_days: int = 5,
    external_infection_prob: float = 0.001,
    initial_infected: int = 3,
    contact_reduction_low: float = 0.4,
    min_attack: float = 0.2,
) -> Tuple[float, float, float, float, float, float]:
    """Run Monte Carlo experiments for Hypothesis 2.

    H2 compares:
      - a high-contact baseline scenario vs.
      - a reduced-contact scenario (simulated via contact_reduction < 1.0)

    It measures:
      - mean day of the infection peak in each scenario, and
      - mean peak infectious count in each scenario,
      then computes the delay in peak timing and the relative reduction
      in peak caseload.
      
    :param daily_edges : dict[int, list[tuple[int, int]]]
        Mapping from day index to a list of (i, j) contact pairs between agents.
    :param num_days : int
        Number of synthetic days to simulate per run (default 120).
    :param num_runs : int
        Number of Monte Carlo runs to average over (default 200).

    :return mean_peak_day_high : float
        Mean peak day in the high-contact scenario.
    :return mean_peak_day_low : float
        Mean peak day in the low-contact scenario.
    :return mean_peak_I_high : float
        Mean peak infectious count in the high-contact scenario.
    :return mean_peak_I_low : float
        Mean peak infectious count in the low-contact scenario.
    :return delay : float
        Average (low - high) peak-day difference (positive means the
        low contact scenario peaks later).
    :return reduction_peak : float
        Relative reduction in peak caseload:
        1 - mean_peak_I_low / mean_peak_I_high

    >>> edges = {0: [(0, 1)]}  # both agents meet on day 0
    >>> result = run_h2(edges, num_days=5, num_runs=5)  # doctest: +ELLIPSIS
    H2:
      Mean peak day (high contacts): ...
      Mean peak day (low contacts): ...
      Delay (days): ...
      Mean peak I (high): ...
      Mean peak I (low): ...
      Relative reduction in peak load: ...
    >>> len(result)
    6
    >>> all(isinstance(x, float) for x in result)
    True
    """
    rng = random.Random(123)
    num_agents = estimate_num_agents(daily_edges)
    households = build_households(num_agents, household_size=4, rng=rng)

    peak_day_high: List[float] = []
    peak_I_high: List[float] = []
    peak_day_low: List[float] = []
    peak_I_low: List[float] = []

    for _ in range(num_runs):
        seq = bootstrap_contact_sequence(daily_edges, num_days=num_days, rng=rng)

        # --- High contacts (baseline) ---
        sim_high = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=infection_prob,
            infectious_days=infectious_days,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=external_infection_prob,
        )
        sim_high.seed_initial_infections(initial_infected)
        I_high, final_R_high = sim_high.run(contact_reduction=1.0)
        attack_high = final_R_high / num_agents

        # --- Low contacts ---
        sim_low = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=infection_prob,
            infectious_days=infectious_days,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=0.0,
            external_infection_prob=external_infection_prob,
        )
        sim_low.seed_initial_infections(initial_infected)
        I_low, final_R_low = sim_low.run(contact_reduction=contact_reduction_low)
        attack_low = final_R_low / num_agents

        # Only keep runs where both scenarios had real outbreaks
        if attack_high >= min_attack and attack_low >= min_attack:
            peak_I_val_high = I_high.max()
            peak_I_high.append(float(peak_I_val_high))
            peak_day_high.append(int(I_high.argmax()))

            peak_I_val_low = I_low.max()
            peak_I_low.append(float(peak_I_val_low))
            peak_day_low.append(int(I_low.argmax()))

    peak_day_high_arr = np.array(peak_day_high)
    peak_I_high_arr = np.array(peak_I_high)
    peak_day_low_arr = np.array(peak_day_low)
    peak_I_low_arr = np.array(peak_I_low)

    mean_peak_day_high = float(peak_day_high_arr.mean())
    mean_peak_day_low = float(peak_day_low_arr.mean())
    mean_peak_I_high = float(peak_I_high_arr.mean())
    mean_peak_I_low = float(peak_I_low_arr.mean())

    delay = mean_peak_day_low - mean_peak_day_high
    reduction_peak = 1 - (mean_peak_I_low / mean_peak_I_high)

    print("H2:")
    print("  Mean peak day (high contacts):", mean_peak_day_high)
    print("  Mean peak day (low contacts):", mean_peak_day_low)
    print("  Delay (days):", delay)
    print("  Mean peak I (high):", mean_peak_I_high)
    print("  Mean peak I (low):", mean_peak_I_low)
    print("  Relative reduction in peak load:", reduction_peak)

    return (
        mean_peak_day_high,
        mean_peak_day_low,
        mean_peak_I_high,
        mean_peak_I_low,
        delay,
        reduction_peak,
    )
