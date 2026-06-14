# ROS2 Usage

This package exposes ROS2 nodes that exchange Phase 2 memory models as JSON
payloads over standard ROS interfaces. The Phase 3 integration intentionally
does not add persistence or recall algorithms yet.

## Nodes

- `memory-recorder` subscribes to `memory/events` as `std_msgs/String` JSON and
  keeps the latest `MemoryEvent` in process memory.
- `trace-publisher` publishes `TaskTrace` values as `std_msgs/String` JSON on
  `memory/traces`.
- `trace-subscriber` subscribes to `memory/traces` and keeps the latest
  `TaskTrace` in process memory.
- `recall-service` exposes `memory/recall` with `std_srvs/Trigger` and returns
  a placeholder response until recall algorithms are implemented.
- `memory-lifecycle` provides lifecycle transition hooks and diagnostic status
  snapshots.

## Launch Examples

Run the core node set:

```sh
ros2 launch memory_aware_ros2_agent memory_pipeline.launch.py
```

Run the lifecycle node:

```sh
ros2 launch memory_aware_ros2_agent memory_lifecycle.launch.py
```

## Parameters

All nodes share these parameters:

- `memory_events_topic`: default `memory/events`
- `memory_traces_topic`: default `memory/traces`
- `recall_service_name`: default `memory/recall`
- `queue_depth`: default `10`
- `namespace`: default empty global namespace

Example:

```sh
ros2 run memory_aware_ros2_agent memory-recorder \
  --ros-args \
  -p memory_events_topic:=robot/memory/events \
  -p queue_depth:=20 \
  -p namespace:=robot
```

## QoS And Callback Groups

Topic nodes build explicit QoS profiles from stable config values. Defaults are
reliable, volatile, keep-last history, and depth from `queue_depth`.

Callback groups default to mutually exclusive execution. Reentrant callback
groups are available through `CallbackGroupConfig` for embedded Python usage.

## Diagnostics

`memory-lifecycle` exposes a `diagnostic_status()` helper that returns a
`diagnostic_msgs/DiagnosticStatus` snapshot with configured, active, and
namespace fields.

## Validation

Use the same commands as CI and phase validation:

```sh
pytest
ruff check .
mypy src
python -m build
colcon build
git status
```
