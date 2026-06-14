# Trace Intelligence Walkthrough

This notebook-style walkthrough shows how to run the default trace intelligence
benchmark dataset, build a benchmark report, and render an experience summary.

```python
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
```

```python
dataset = default_trace_analyzer_benchmark_dataset()
report = build_trace_analyzer_benchmark_report(dataset)
print(render_trace_analyzer_benchmark_report(report))
```

```python
first_case = dataset.cases[0]
summary = summarize_experience(first_case.trace)
print(render_experience_summary(summary))
```

Expected report output:

```text
Trace Analyzer Benchmark: default-trace-intelligence
Cases: 3
Status accuracy: 1.00
Failure pattern accuracy: 1.00
Anomaly accuracy: 1.00
```
