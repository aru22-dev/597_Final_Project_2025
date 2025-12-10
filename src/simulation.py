import numpy as np
import random
from typing import List, Tuple, Dict

S, I, R = 0, 1, 2  # simple SIR for clarity

class EpidemicSimulation:
    def __init__(
        self,
        num_agents: int,
        contact_sequence: List[List[Tuple[int, int]]],
        infection_prob: float,
        infectious_days: int,
        rng: random.Random,
        households=None,
        isolate_symptomatic: bool = False,
        isolate_households: bool = False,
        vaccination_coverage: float = 0.0,
        external_infection_prob: float = 0.0,
    ):
        self.num_agents = num_agents
        self.contact_sequence = contact_sequence
        self.T = len(contact_sequence)
        self.infection_prob = infection_prob
        self.infectious_days = infectious_days
        self.rng = rng

        self.households = households
        self.isolate_symptomatic = isolate_symptomatic
        self.isolate_households = isolate_households
        self.external_infection_prob = external_infection_prob

        self.state = np.full(num_agents, S, dtype=int)
        self.days_in_state = np.zeros(num_agents, dtype=int)

        # Vaccination
        if vaccination_coverage > 0.0:
            n_vax = int(num_agents * vaccination_coverage)
            vaccinated_idxs = rng.sample(range(num_agents), n_vax)
            for idx in vaccinated_idxs:
                self.state[idx] = R

    def seed_initial_infections(self, num_initial: int = 3):
        """
        Seed the population with an initial set of infected individuals.

        If the requested number of initial infections is larger than the number
        of susceptible individuals available, this method will automatically
        reduce num_initial to avoid errors.

        This makes the simulation robust for very small test networks, such as
        the toy example used in doctests.
        """
        susceptible = np.where(self.state == S)[0]

        if len(susceptible) == 0:
             return  # nothing to infect

        # Clamp num_initial to the number of susceptibles
        if num_initial > len(susceptible):
            num_initial = len(susceptible)

        infected = self.rng.sample(list(susceptible), num_initial)
        for idx in infected:
            self.state[idx] = I
            self.days_in_state[idx] = 0


    def _get_isolated_mask(self):
        isolated = np.zeros(self.num_agents, dtype=bool)

    # Only isolate symptomatic infections if enabled
        if self.isolate_symptomatic:
        # "symptomatic" = infectious for at least 1 day
            infectious_idxs = np.where((self.state == I) & (self.days_in_state >= 1))[0]
            isolated[infectious_idxs] = True

    # Household isolation: if any infectious in HH, isolate entire HH
        if self.isolate_households and self.households is not None:
            for hh in self.households:
                if any(self.state[i] == I for i in hh):
                    for i in hh:
                        isolated[i] = True

        return isolated

    def step(self, day: int, contact_reduction: float = 1.0):
        edges = self.contact_sequence[day]

        # 1. External infections from untracked population
        new_infected = []
        if self.external_infection_prob > 0:
            for person in range(self.num_agents):
                if self.state[person] == S and self.rng.random() < self.external_infection_prob:
                    new_infected.append(person)

        # 2. Apply isolation
        isolated = self._get_isolated_mask()
        active_edges = [(i, j) for (i, j) in edges if not isolated[i] and not isolated[j]]

        # 3. Apply contact reduction
        if 0 < contact_reduction < 1.0 and len(active_edges) > 0:
            k = int(len(active_edges) * contact_reduction)
            k = max(k, 0)
            active_edges = self.rng.sample(active_edges, k)

        # 4. Transmission via observed contacts
        for (i, j) in active_edges:
            if self.state[i] == I and self.state[j] == S and self.rng.random() < self.infection_prob:
                new_infected.append(j)
            if self.state[j] == I and self.state[i] == S and self.rng.random() < self.infection_prob:
                new_infected.append(i)

        for p in new_infected:
            if self.state[p] == S:
                self.state[p] = I
                self.days_in_state[p] = 0

        # 5. Progression I to R
        for p in range(self.num_agents):
            if self.state[p] == I:
                self.days_in_state[p] += 1
                if self.days_in_state[p] >= self.infectious_days:
                    self.state[p] = R
                    self.days_in_state[p] = 0


        # Transmission
        new_infected = []
        for (i, j) in active_edges:
            # symmetrical contacts
            if self.state[i] == I and self.state[j] == S and self.rng.random() < self.infection_prob:
                new_infected.append(j)
            if self.state[j] == I and self.state[i] == S and self.rng.random() < self.infection_prob:
                new_infected.append(i)

        for p in new_infected:
            if self.state[p] == S:
                self.state[p] = I
                self.days_in_state[p] = 0

        # Progression I -> R
        for p in range(self.num_agents):
            if self.state[p] == I:
                self.days_in_state[p] += 1
                if self.days_in_state[p] >= self.infectious_days:
                    self.state[p] = R
                    self.days_in_state[p] = 0

    def run(self, contact_reduction: float = 1.0):
        history_I = []

        for day in range(self.T):
            history_I.append(np.sum(self.state == I))
            self.step(day, contact_reduction=contact_reduction)

        history_I = np.array(history_I)
        final_R = np.sum(self.state == R)
        return history_I, final_R
