import random
from typing import Dict, List, Tuple
import numpy as np
from src.simulation import EpidemicSimulation
from src.helpers import build_households, bootstrap_contact_sequence, estimate_num_agents

def run_h1(
    daily_edges: Dict[int, List[Tuple[int, int]]],
    num_days: int = 120,
    num_runs: int = 100,
    infection_prob: float = 0.03,
    infectious_days: int = 5,
    external_infection_prob: float = 0.001,
    initial_infected: int = 3,
):
    """Run Monte Carlo experiments for Hypothesis 1.

    H1 compares:
      - individual isolation of symptomatic cases vs.
      - household level isolation (isolating the whole household of a symptomatic case)

    :param daily_edges : Mapping from day index to a list of (i, j) contact pairs between agents
    :param num_days : Number of synthetic days to simulate per run (default 120)
    :param num_runs : Number of Monte Carlo runs to average over (default 100)

    :returns mean_individual : Mean total infections when only symptomatic individuals are isolated.
    :returns mean_household : Mean total infections when symptomatic individuals and their households are isolated.
    :returns reduction : Relative reduction in infections from household isolation: 1 - mean_household / mean_individual

    >>> edges = {0: [(0, 1)]}  # both agents meet on day 0
    >>> mean_ind, mean_hh, red = run_h1(edges, num_days=5, num_runs=5)  # doctest: +ELLIPSIS
    H1:
      Mean total infections (individual isolation): ...
      Mean total infections (household isolation): ...
      Relative reduction: ...
    >>> isinstance(mean_ind, float)
    True
    >>> isinstance(mean_hh, float)
    True
    >>> isinstance(red, float)
    True
    >>> bool(np.isnan(red))
    False
    """
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
        infection_prob=infection_prob,
        infectious_days=infectious_days,
        rng=rng,
        households=households,
        isolate_symptomatic=True,
        isolate_households=False,
        vaccination_coverage=0.0,
        external_infection_prob=external_infection_prob,
    )
        simA.seed_initial_infections(initial_infected)
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
    return mean_individual, mean_household, reduction
