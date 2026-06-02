from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from domain import Domain, Offer, UtilityFunction
from strategies import NegotiationState, Strategy


@dataclass
class NegotiationAgent:
    name: str
    domain: Domain
    utility_function: UtilityFunction
    strategy: Strategy
    minimum_utility_threshold: float = 0.7
    _sorted_offers: List[Tuple[Offer, float]] = field(default_factory=list)

    def __post_init__(self) -> None:
        offers = self.domain.all_offers()
        scored = [(offer, self.utility_function.evaluate(offer)) for offer in offers]
        scored.sort(key=lambda x: x[1], reverse=True)
        self._sorted_offers = scored

    def utility(self, offer: Offer) -> float:
        return self.utility_function.evaluate(offer)

    def current_aspiration(self, state: NegotiationState) -> float:
        return max(self.minimum_utility_threshold, self.strategy.aspiration(state))

    def choose_offer(self, state: NegotiationState) -> Offer:
        target = self.current_aspiration(state)

        # Choose the lowest-utility own offer that still satisfies the current aspiration.
        for offer, utility in reversed(self._sorted_offers):
            if utility >= target:
                return offer

        # If nothing satisfies the current aspiration, choose the lowest-utility offer
        # that is still above the minimum threshold.
        for offer, utility in reversed(self._sorted_offers):
            if utility >= self.minimum_utility_threshold:
                return offer

        # Worst-case fallback
        return self._sorted_offers[-1][0]

    def should_accept(self, offer: Offer, state: NegotiationState) -> bool:
        return self.utility(offer) >= self.current_aspiration(state)