from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import random
from typing import Dict, List, Tuple


IssueValue = int
Offer = Tuple[IssueValue, ...]


@dataclass
class Domain:
    """
    Multi-issue discrete negotiation domain.
    Example:
        issues = [5, 4, 3]
    means:
        - issue 0 has values 0..4
        - issue 1 has values 0..3
        - issue 2 has values 0..2
    """
    issue_sizes: List[int]

    def all_offers(self) -> List[Offer]:
        ranges = [range(size) for size in self.issue_sizes]
        return list(product(*ranges))


@dataclass
class UtilityFunction:
    """
    Additive weighted utility function.
    weights[i] = importance of issue i
    value_utils[i][v] = utility of choosing value v for issue i
    """
    weights: List[float]
    value_utils: List[Dict[int, float]]

    def evaluate(self, offer: Offer) -> float:
        total = 0.0
        for i, value in enumerate(offer):
            total += self.weights[i] * self.value_utils[i][value]
        return total


def normalize_weights(weights: List[float]) -> List[float]:
    s = sum(weights)
    return [w / s for w in weights]


def random_utility_function(domain: Domain, rng: random.Random) -> UtilityFunction:
    raw_weights = [rng.random() for _ in domain.issue_sizes]
    weights = normalize_weights(raw_weights)

    value_utils: List[Dict[int, float]] = []
    for size in domain.issue_sizes:
        vals = list(range(size))
        raw_scores = [rng.random() for _ in vals]
        max_score = max(raw_scores) if raw_scores else 1.0
        normalized = [x / max_score for x in raw_scores]
        value_utils.append({v: u for v, u in zip(vals, normalized)})

    return UtilityFunction(weights=weights, value_utils=value_utils)


def random_domain(
    num_issues: int = 3,
    min_issue_size: int = 3,
    max_issue_size: int = 5,
    rng: random.Random | None = None,
) -> Domain:
    rng = rng or random.Random()
    issue_sizes = [rng.randint(min_issue_size, max_issue_size) for _ in range(num_issues)]
    return Domain(issue_sizes=issue_sizes)