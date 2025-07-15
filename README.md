# STACKWALKER

A Python library for bidirectional call stack inspection and frame analysis. Provides utilities for walking through Python's call stack in both directions - from current frame to callers (backward) and from root to current frame (forward).

## Features

-   **Bidirectional Navigation**: Navigate call stack both backward (to callers) and forward (from root)
-   **Frame Information Extraction**: Get function names, line numbers, and module information
-   **Safe Frame Handling**: Graceful error handling with sensible defaults
-   **Flexible Frame Search**: Find frames by function name and module
-   **Complete Stack Analysis**: Collect and analyze entire call stacks

## Installation

```bash
pip install frame-info
```

## Quick Start

```python
from stackwalker import stackwalker

def caller_function():
    target_function()

def target_function():
    # Get current frame info
    current = stackwalker.get_frame_by_index(0)
    print(f"Current: {current['caller_name']}")  # target_function

    # Get caller frame info
    caller = stackwalker.get_frame_by_index(-1)
    print(f"Caller: {caller['caller_name']}")   # caller_function

    # Get complete frame list
    frames = stackwalker.get_frame_list()
    for frame in frames:
        print(f"{frame['caller_name']} at line {frame['caller_line']}")
```

## API Reference

### Core Functions

#### `get_frame_by_index(index: int)`

Get frame information by index position.

-   `index = 0`: Current frame
-   `index < 0`: Navigate backward to callers (-1 = immediate caller)
-   `index > 0`: Navigate forward from root caller

#### `get_frame_by_name(caller_name: str, module_name: str, offset: int = 1)`

Find a frame by function and module name.

#### `get_frame_list()`

Get complete list of all frames in the call stack.

#### `get_frame_name_list()`

Get list of (module_name, function_name) tuples for all frames.

### Frame Information Structure

Each frame returns a dictionary with:

```python
{
    'caller_name': str,      # Function name
    'caller_line': int,      # Line number
    'module_name': str,      # Module name
    'caller_locals': dict,   # Local variables
    'caller_filename': str   # Source filename
}
```

## Use Cases

-   **Debugging Tools**: Build sophisticated debugging utilities
-   **Logging Systems**: Automatic caller detection for logs
-   **Code Analysis**: Analyze call patterns and stack traces
-   **Testing Utilities**: Inspect test execution context
-   **Profiling**: Track function call hierarchies

## Frame Index Reference

```
Call Stack:     Frame Index:
                Negative  Positive
main()          -3        1
├─ func_a()     -2        2
   ├─ func_b()  -1        3
      └─ here   0         4 (current)
```

## Requirements

-   Python 3.8+
-   Works with standard Python implementations that support `inspect.currentframe()`

## Testing

```bash
# Using unittest
python -m unittest tests.test_stackwalker

# Using pytest
pytest tests/test_stackwalker.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please read the contributing guidelines and submit pull
