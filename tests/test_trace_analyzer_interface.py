from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.trace_intelligence import TraceAnalyzer, TraceInsight


class StubTraceAnalyzer:
    def analyze(self, trace: TaskTrace) -> TraceInsight:
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="stub",
            summary=f"Analyzed {trace.task_name}",
        )


def test_trace_analyzer_protocol_returns_trace_insight() -> None:
    analyzer: TraceAnalyzer = StubTraceAnalyzer()
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="dock",
        started_at="2026-06-14T10:00:00Z",
    )

    insight = analyzer.analyze(trace)

    assert insight == TraceInsight(
        trace_id="trace-001",
        insight_type="stub",
        summary="Analyzed dock",
    )
