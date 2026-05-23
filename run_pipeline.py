from src.data_quality import check_data_quality
from src.trend_analysis import plot_publication_trend
from src.word_cloud_analysis import generate_word_cloud
from src.metrics_analysis import calculate_metrics
from src.milestone_papers import build_milestone_candidates
from src.keyword_cooccurrence import build_keyword_cooccurrence
from src.network_analysis import (
    build_author_network,
    build_institution_network,
    build_reference_citation_network,
)
from src.sensitivity_analysis import run_sensitivity_analysis


def main():
    print("=" * 72)
    print("LLM multi-agent bibliometric analysis pipeline")
    print("=" * 72)

    steps = [
        ("M1 data quality and cleaned dataset", check_data_quality),
        ("M1 annual publication trend", plot_publication_trend),
        ("M1 title word cloud", generate_word_cloud),
        ("M2 bibliometric indicators", calculate_metrics),
        ("M2 milestone paper candidates", build_milestone_candidates),
        ("M2 keyword co-occurrence network", build_keyword_cooccurrence),
        ("M2 author collaboration network", build_author_network),
        ("M2 institution/country distribution", build_institution_network),
        ("M2 citation reference network", build_reference_citation_network),
        ("M2 parameter sensitivity analysis", run_sensitivity_analysis),
    ]

    for index, (name, func) in enumerate(steps, 1):
        print(f"\n[{index}/{len(steps)}] {name}")
        func()

    print("\nPipeline completed. Check outputs/, outputs/figures/, and reports/.")


if __name__ == "__main__":
    main()
