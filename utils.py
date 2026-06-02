import csv
from collections import defaultdict
from dataclasses import asdict
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import math

from session import NegotiationResult


def save_results_to_csv(results: List[NegotiationResult], filename: str = "results.csv") -> None:
    """
    Save raw negotiation results to a CSV file.
    """
    if not results:
        return

    keys = asdict(results[0]).keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()

        for r in results:
            writer.writerow(asdict(r))


def summarize_results(results: List[NegotiationResult], combine_symmetric: bool = False) -> Dict[Tuple[str, str], dict]:
    grouped: Dict[Tuple[str, str], List[NegotiationResult]] = defaultdict(list)

    for r in results:
        if combine_symmetric:
            key = _canonical_pair(r.strategy_a, r.strategy_b)
        else:
            key = (r.strategy_a, r.strategy_b)
        grouped[key].append(r)

    summary: Dict[Tuple[str, str], dict] = {}

    for key, group in grouped.items():
        n = len(group)

        agreement_values = [1 if r.agreement_reached else 0 for r in group]
        rounds_values = [r.rounds_used for r in group]
        welfare_values = [r.social_welfare for r in group]
        ua_values = [r.utility_agent_a for r in group]
        ub_values = [r.utility_agent_b for r in group]

        agreement_stats = compute_confidence_interval(agreement_values)
        rounds_stats = compute_confidence_interval(rounds_values)
        welfare_stats = compute_confidence_interval(welfare_values)
        ua_stats = compute_confidence_interval(ua_values)
        ub_stats = compute_confidence_interval(ub_values)

        summary[key] = {
            "n_sessions": n,

            "agreement_rate_mean": agreement_stats["mean"],
            "agreement_rate_ci": agreement_stats["ci95"],

            "avg_rounds_mean": rounds_stats["mean"],
            "avg_rounds_ci": rounds_stats["ci95"],

            "avg_social_welfare_mean": welfare_stats["mean"],
            "avg_social_welfare_ci": welfare_stats["ci95"],

            "avg_utility_a_mean": ua_stats["mean"],
            "avg_utility_a_ci": ua_stats["ci95"],

            "avg_utility_b_mean": ub_stats["mean"],
            "avg_utility_b_ci": ub_stats["ci95"],
        }

    return summary


def print_summary(summary):
    print("=== TOURNAMENT SUMMARY ===")
    for (strategy_a, strategy_b), stats in sorted(summary.items()):
        print(f"\n{strategy_a} vs {strategy_b}")
        print(f"  n_sessions: {stats['n_sessions']}")
        print(f"  agreement_rate: {stats['agreement_rate_mean']:.4f} ± {stats['agreement_rate_ci']:.4f}")
        print(f"  avg_rounds: {stats['avg_rounds_mean']:.4f} ± {stats['avg_rounds_ci']:.4f}")
        print(f"  avg_social_welfare: {stats['avg_social_welfare_mean']:.4f} ± {stats['avg_social_welfare_ci']:.4f}")


def _group_metric(
    results: List[NegotiationResult],
    metric_name: str,
    combine_symmetric: bool = False
) -> Tuple[List[str], List[float]]:
    grouped = defaultdict(list)

    for r in results:
        if combine_symmetric:
            a, b = _canonical_pair(r.strategy_a, r.strategy_b)
            key = f"{a} vs {b}"
        else:
            key = f"{r.strategy_a} vs {r.strategy_b}"

        if metric_name == "agreement_rate":
            grouped[key].append(1 if r.agreement_reached else 0)
        elif metric_name == "social_welfare":
            grouped[key].append(r.social_welfare)
        elif metric_name == "rounds_used":
            grouped[key].append(r.rounds_used)
        else:
            raise ValueError(f"Unknown metric_name: {metric_name}")

    labels = []
    values = []

    for k, v in grouped.items():
        labels.append(k.replace(" vs ", "\n"))
        values.append(sum(v) / len(v))

    return labels, values


def plot_agreement_rate(results: List[NegotiationResult], save_path: str | None = None, combine_symmetric: bool = False) -> None:
    labels, values = _group_metric(results, "agreement_rate", combine_symmetric=combine_symmetric)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Agreement Rate")
    plt.title("Agreement Rate by Strategy Pair")
    plt.ylim(0, 1.05)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_social_welfare(results: List[NegotiationResult], save_path: str | None = None, combine_symmetric: bool = False) -> None:
    labels, values = _group_metric(results, "social_welfare", combine_symmetric=combine_symmetric)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Average Social Welfare")
    plt.title("Average Social Welfare by Strategy Pair")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_rounds(results: List[NegotiationResult], save_path: str | None = None, combine_symmetric: bool = False) -> None:
    labels, values = _group_metric(results, "rounds_used", combine_symmetric=combine_symmetric)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Average Rounds")
    plt.title("Average Negotiation Length by Strategy Pair")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()

def _canonical_pair(strategy_a: str, strategy_b: str) -> tuple[str, str]:
    return tuple(sorted((strategy_a, strategy_b)))

def compute_confidence_interval(values: list[float]) -> dict:
    """
    Compute mean, standard deviation, standard error,
    and 95% confidence interval for a list of values.
    """
    n = len(values)

    if n == 0:
        return {
            "mean": 0.0,
            "std": 0.0,
            "stderr": 0.0,
            "ci95": 0.0,
        }

    mean = sum(values) / n

    # Sample standard deviation (ddof=1)
    variance = sum((x - mean) ** 2 for x in values) / (n - 1 if n > 1 else 1)
    std = math.sqrt(variance)

    stderr = std / math.sqrt(n)

    # 95% confidence interval
    ci95 = 1.96 * stderr

    return {
        "mean": mean,
        "std": std,
        "stderr": stderr,
        "ci95": ci95,
    }