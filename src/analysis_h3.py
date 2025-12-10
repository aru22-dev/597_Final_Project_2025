import random
from typing import Dict, List, Tuple

import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents


def run_h3(
    daily_edges: Dict[int, List[Tuple[int, int]]],
    num_days: int = 120,
    num_runs: int = 300,
    infection_prob: float = 0.09,
    infectious_days: int = 5,
    external_infection_prob: float = 0.001,
    initial_infected: int = 3,
    vaccination_coverage: float = 0.30,
    large_outbreak_thresh: float = 0.5,
) -> Tuple[float, float, float]:
    """Run Monte Carlo experiments for Hypothesis 3.

    H3 compares:
      - the probability of a "large outbreak" (attack rate >= 50%)
        with no vaccination vs.
      - the probability of a large outbreak when 30% of the population
        is pre emptively vaccinated.

    It estimates:
      - P(large outbreak) with no vaccination,
      - P(large outbreak) with 30% vaccination, and
      - the relative reduction between them.

    :param daily_edges : dict[int, list[tuple[int, int]]]
        Mapping from day index to a list of (i, j) contact pairs between agents.
    :param num_days : int
        Number of synthetic days to simulate per run (default 120).
    :param num_runs : int
        Number of Monte Carlo runs to average over (default 300).

    :return p_no : float
        Estimated probability of a large outbreak without vaccination.
    :return p_vax : float
        Estimated probability of a large outbreak with 30% vaccination.
    :return reduction_prob : float
        Relative reduction: 1 - p_vax / p_no, or NaN if p_no == 0.

    >>> edges = {0: [(0, 1)]}  # both agents meet on day 0
    >>> p_no, p_vax, red = run_h3(edges, num_days=5, num_runs=5)  # doctest: +ELLIPSIS
    H3:
      P(large outbreak) no vax: ...
      P(large outbreak) 30% vax: ...
      Relative reduction: ...
    >>> isinstance(p_no, float)
    True
    >>> isinstance(p_vax, float)
    True
    >>> isinstance(red, float)
    True
    """
    rng = random.Random(999)
    num_agents = estimate_num_agents(daily_edges)
    households = build_households(num_agents, household_size=4, rng=rng)

    large_no_vax: List[bool] = []
    large_vax: List[bool] = []

    for _ in range(num_runs):
        seq = bootstrap_contact_sequence(daily_edges, num_days=num_days, rng=rng)

        # --- No vaccination ---
        sim_no = EpidemicSimulation(
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
        sim_no.seed_initial_infections(initial_infected)
        I_no, final_R_no = sim_no.run(contact_reduction=1.0)
        attack_no = final_R_no / num_agents
        large_no_vax.append(attack_no >= large_outbreak_thresh)

        # --- Vaccination scenario ---
        sim_vax = EpidemicSimulation(
            num_agents=num_agents,
            contact_sequence=seq,
            infection_prob=infection_prob,
            infectious_days=infectious_days,
            rng=rng,
            households=households,
            isolate_symptomatic=False,
            isolate_households=False,
            vaccination_coverage=vaccination_coverage,
            external_infection_prob=external_infection_prob,
        )
        sim_vax.seed_initial_infections(initial_infected)
        I_vax, final_R_vax = sim_vax.run(contact_reduction=1.0)
        attack_vax = final_R_vax / num_agents
        large_vax.append(attack_vax >= large_outbreak_thresh)

    large_no_vax_arr = np.array(large_no_vax, dtype=bool)
    large_vax_arr = np.array(large_vax, dtype=bool)

    p_no = float(large_no_vax_arr.mean())
    p_vax = float(large_vax_arr.mean())

    if p_no == 0.0:
        reduction_prob = float("nan")
    else:
        reduction_prob = 1 - (p_vax / p_no)

    print("H3:")
    print("  P(large outbreak) no vax:", p_no)
    print("  P(large outbreak) 30% vax:", p_vax)
    print("  Relative reduction:", reduction_prob)

    return p_no, p_vax, reduction_prob
