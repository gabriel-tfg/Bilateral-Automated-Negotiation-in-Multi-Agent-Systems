from __future__ import annotations

import random
from itertools import combinations_with_replacement
from typing import Callable, Dict, List

from agent import NegotiationAgent
from domain import random_domain, random_utility_function
from session import NegotiationResult, NegotiationSession
from strategies import BoulwareStrategy, ConcederStrategy, LinearStrategy, Strategy


StrategyFactory = Callable[[], Strategy]


def run_tournament(
    num_domains: int = 50,
    max_rounds: int = 30,
    seed: int = 42,
    minimum_utility_threshold: float = 0.7,
) -> List[NegotiationResult]:
    rng = random.Random(seed)

    strategy_factories: Dict[str, StrategyFactory] = {
        "Boulware": BoulwareStrategy,
        "Conceder": ConcederStrategy,
        "Linear": LinearStrategy,
    }

    results: List[NegotiationResult] = []
    strategy_names = list(strategy_factories.keys())

    # 6 unordered pairs instead of 9 ordered pairs
    unordered_pairs = list(combinations_with_replacement(strategy_names, 2))

    for _ in range(num_domains):
        domain = random_domain(num_issues=3, min_issue_size=3, max_issue_size=5, rng=rng)

        for s1, s2 in unordered_pairs:
            uf1 = random_utility_function(domain, rng)
            uf2 = random_utility_function(domain, rng)

            agent_a = NegotiationAgent(
                name="AgentA",
                domain=domain,
                utility_function=uf1,
                strategy=strategy_factories[s1](),
                minimum_utility_threshold=minimum_utility_threshold,
            )
            agent_b = NegotiationAgent(
                name="AgentB",
                domain=domain,
                utility_function=uf2,
                strategy=strategy_factories[s2](),
                minimum_utility_threshold=minimum_utility_threshold,
            )

            # Randomize who starts
            if rng.random() < 0.5:
                first_agent, second_agent = agent_a, agent_b
            else:
                first_agent, second_agent = agent_b, agent_a

            session = NegotiationSession(first_agent, second_agent, max_rounds=max_rounds)
            result = session.run()
            results.append(result)

    return results