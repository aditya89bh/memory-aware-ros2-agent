"""Run a small trace intelligence demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memory_aware_ros2_agent.trace_intelligence import summarize_experience
from memory_aware_ros2_agent.trace_intelligence_benchmarks import (
    default_trace_analyzer_benchmark_dataset,
)
from memory_aware_ros2_agent.trace_intelligence_reports import (
    build_trace_analyzer_benchmark_report,
)
from memory_aware_ros2_agent.trace_intelligence_visualizations import (
    render_experience_summary,
    render_trace_analyzer_benchmark_report,
)


def main() -> None:
    """Print trace intelligence summaries for the default benchmark dataset."""

    dataset = default_trace_analyzer_benchmark_dataset()
    report = build_trace_analyzer_benchmark_report(dataset)
    print(render_trace_analyzer_benchmark_report(report))
    print()
    for case in dataset.cases:
        print(render_experience_summary(summarize_experience(case.trace)))
        print()


if __name__ == "__main__":
    main()
