# helpers.py
import random
from typing import Dict, List, Tuple
import numpy as np

def build_households(num_agents: int, household_size: int, rng: random.Random):
    idxs = list(range(num_agents))
    rng.shuffle(idxs)
    households = []
    for i in range(0, num_agents, household_size):
        households.append(idxs[i:i+household_size])
    return households

def bootstrap_contact_sequence(
    daily_edges: Dict[int, List[Tuple[int, int]]],
    num_days: int,
    rng: random.Random
) -> List[List[Tuple[int, int]]]:
    day_keys = list(daily_edges.keys())
    seq = []
    for _ in range(num_days):
        d = rng.choice(day_keys)
        seq.append(daily_edges[d])
    return seq

def estimate_num_agents(daily_edges):
    ids = set()
    for edges in daily_edges.values():
        for i, j in edges:
            ids.add(i); ids.add(j)
    return max(ids) + 1

