from tournament import run_tournament
from utils import (
    save_results_to_csv,
    summarize_results,
    print_summary,
    plot_agreement_rate,
    plot_social_welfare,
    plot_rounds,
)


def main() -> None:
    # Larger experimental setting
    num_domains = 10000   # 10,000 domains x 6 unordered pairs = 60,000 negotiations
    max_rounds = 12
    seed = 123
    minimum_utility_threshold: float = 0.7

    results = run_tournament(
        num_domains=num_domains,
        max_rounds=max_rounds,
        seed=seed,
        minimum_utility_threshold=minimum_utility_threshold,
    )

    save_results_to_csv(results, "results_large.csv")

    summary = summarize_results(results, combine_symmetric=True)
    print_summary(summary)

    plot_agreement_rate(results, save_path="agreement_rate_large.png", combine_symmetric=True)
    plot_social_welfare(results, save_path="social_welfare_large.png", combine_symmetric=True)
    plot_rounds(results, save_path="rounds_large.png", combine_symmetric=True)


if __name__ == "__main__":
    main()