from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from agent import NegotiationAgent
from domain import Offer
from strategies import NegotiationState


@dataclass
class NegotiationResult:
    agreement_reached: bool
    accepted_offer: Optional[Offer]
    rounds_used: int
    utility_agent_a: float
    utility_agent_b: float
    social_welfare: float
    agent_a_name: str
    agent_b_name: str
    strategy_a: str
    strategy_b: str


class NegotiationSession:
    def __init__(self, agent_a: NegotiationAgent, agent_b: NegotiationAgent, max_rounds: int = 30):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.max_rounds = max_rounds

    def run(self) -> NegotiationResult:
        current_proposer = self.agent_a
        current_responder = self.agent_b

        for round_number in range(self.max_rounds):
            state = NegotiationState(round_number=round_number, max_rounds=self.max_rounds)
            offer = current_proposer.choose_offer(state)

            if current_responder.should_accept(offer, state):
                ua = self.agent_a.utility(offer)
                ub = self.agent_b.utility(offer)
                return NegotiationResult(
                    agreement_reached=True,
                    accepted_offer=offer,
                    rounds_used=round_number + 1,
                    utility_agent_a=ua,
                    utility_agent_b=ub,
                    social_welfare=ua + ub,
                    agent_a_name=self.agent_a.name,
                    agent_b_name=self.agent_b.name,
                    strategy_a=self.agent_a.strategy.name,
                    strategy_b=self.agent_b.strategy.name,
                )

            current_proposer, current_responder = current_responder, current_proposer

        return NegotiationResult(
            agreement_reached=False,
            accepted_offer=None,
            rounds_used=self.max_rounds,
            utility_agent_a=0.0,
            utility_agent_b=0.0,
            social_welfare=0.0,
            agent_a_name=self.agent_a.name,
            agent_b_name=self.agent_b.name,
            strategy_a=self.agent_a.strategy.name,
            strategy_b=self.agent_b.strategy.name,
        )