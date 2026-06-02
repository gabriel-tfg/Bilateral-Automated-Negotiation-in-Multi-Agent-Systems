from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class NegotiationState:
    round_number: int
    max_rounds: int

    @property
    def time_fraction(self) -> float:
        if self.max_rounds <= 1:
            return 1.0
        return self.round_number / (self.max_rounds - 1)


class Strategy(ABC):
    name: str = "BaseStrategy"

    @abstractmethod
    def aspiration(self, state: NegotiationState) -> float:
        """
        Returns the minimum utility target at a given time.
        Assumed normalized in [0, 1].
        """
        raise NotImplementedError


class LinearStrategy(Strategy):
    name = "Linear"

    def aspiration(self, state: NegotiationState) -> float:
        t = state.time_fraction
        return 1.0 - 0.9 * t


class ConcederStrategy(Strategy):
    name = "Conceder"

    def aspiration(self, state: NegotiationState) -> float:
        t = state.time_fraction
        return 1.0 - 0.9 * (t ** 0.5)


class BoulwareStrategy(Strategy):
    name = "Boulware"

    def aspiration(self, state: NegotiationState) -> float:
        t = state.time_fraction
        return 1.0 - 0.9 * (t ** 3.0)