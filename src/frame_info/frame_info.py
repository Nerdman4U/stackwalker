"""
Core utilities for bidirectional frame inspection and debugging.

This module provides low-level utilities for inspecting Python's call stack with
support for both forward and backward navigation. It enables automatic detection
of caller context for logging, debugging, and code generation purposes.

The frame inspection utilities allow you to walk in both directions through the
call stack to identify calling functions, their line numbers, and other execution
context information. This is particularly useful for creating debugging tools
and logging systems that need to show meaningful caller information.

Features:
    - Bidirectional frame navigation (backwards to callers, forwards to callees)
    - Complete call stack collection and analysis
    - Safe frame inspection with graceful error handling
    - Function name and line number extraction utilities

Functions:
    _collect_frame_stack: Collect all frames in the current call stack
    _get_frame: Navigate through the call stack by a specified index (bidirectional)
    _get_frame_name: Extract the function name from a frame object
    _get_frame_line: Extract the line number from a frame object

Example:
    Basic frame inspection:

        def caller_function():          # Frame -2 (index 2 from root)
            target_function()

        def target_function():          # Frame -1 (index 1 from root)
            # Get different frames using index
            current = _get_frame(0)     # target_function
            caller = _get_frame(-1)     # caller_function
            root = _get_frame(-2)       # __main__

            # Forward navigation (from root)
            root_alt = _get_frame(1)    # __main__ (deepest caller)
            caller_alt = _get_frame(2)  # caller_function (second frame)

    Complete call stack analysis:

        def level1():
            level2()

        def level2():
            level3()

        def level3():
            frames = _collect_frame_stack()
            for i, frame in enumerate(frames):
                name = _get_frame_name(frame)
                line = _get_frame_line(frame)
                print(f"Frame {i}: {name}:{line}")

    Output:
        Frame 0: level3:45
        Frame 1: level2:42
        Frame 2: level1:39
        Frame 3: __main__:50

Frame index Reference:
    Negative index (backward navigation):
        -1: immediate caller
        -2: caller's caller
        -3: caller's caller's caller

    Positive index (forward navigation from root):
        +1: deepest caller (root of call stack)
        +2: second frame from root
        +3: third frame from root

    Zero index:
        0: current frame

Notes:
    - Frame index use collected stack for efficient bidirectional navigation
    - Functions gracefully handle missing frames by returning safe defaults
    - Primarily used by logging and debugging utilities in this package
    - Uses inspect.currentframe() which may not be available in all Python implementations
    - Forward navigation is implemented by collecting the full stack and indexing from the end
"""
import inspect
from typing import Any
from types import FrameType


def _collect_frame_stack() -> list[FrameType]:
    """Collect all frames in the current call stack.

    Returns:
        list: List of frames from current (index 0) to root caller
    """
    frames = []
    frame = inspect.currentframe()
    while frame:
        frames.append(frame)
        frame = frame.f_back
    return frames


def __get_frame(frame_index: int = -1) -> FrameType | None:
    """Get frame with bidirectional navigation using collected stack.

    Args:
        frame_index (int): index from current frame
            - 0: current frame
            - -1: immediate caller (1 step back)
            - -2: caller's caller (2 steps back)
            - +1: first frame in stack (deepest caller)
            - +2: second frame in stack
    """
    frames = _collect_frame_stack()

    if not frames:
        return None

    if frame_index == 0:
        return frames[0]  # Current frame

    if frame_index < 0:
        # Negative = go backwards (normal behavior)
        index = abs(frame_index)
        return frames[index] if index < len(frames) else None

    if frame_index > 0:
        # Positive = go from the end (root caller direction)
        index = len(frames) - frame_index
        return frames[index] if index >= 0 else None

    return None


def __get_frame_name(frame: FrameType) -> str:
    """Get function name from a frame object."""
    return frame.f_code.co_name if frame else "Unknown"


def __get_frame_line(frame: FrameType) -> int:
    """Get line number from a frame object."""
    return frame.f_lineno if frame else 0


def __get_module_name(frame: FrameType) -> str:
    """Get module name from a frame object.

    Args:
        frame (FrameType): Frame object to extract module name from.

    Returns:
        str: Module name or "Unknown" if not available.
    """
    return frame.f_globals.get("__name__", "Unknown") if frame else "Unknown"


def get_frame_info(index) -> dict[str, Any]:
    """Get frame name and line number from a frame object.

    Args:
        index (int): index of frame stack.

    Returns:
        tuple: (function name, line number)
    """
    frame = __get_frame(index)
    if not frame:
        return {
            "frame": None,
            "caller_name": "Unknown",
            "caller_line": 0,
            "module_name": "Unknown"
        }

    return {
        "frame": frame,
        "caller_name": __get_frame_name(frame),
        "caller_line": __get_frame_line(frame),
        "module_name": __get_module_name(frame)
    }


if __name__ == "__main__":
    def test1(index):
        """Building frames for testing"""
        test2(index)

    def test2(index):
        """Building frames for testing"""
        __frame = __get_frame(index)
        if not __frame:
            print(f"No frame found for index: {index}")
            return
        __frame_name = __get_frame_name(__frame)
        __frame_line = __get_frame_line(__frame)
        print(f"index: {index}, Name: {__frame_name}, Line: {__frame_line}")

    # Test different indexes
    print("=== Frame Navigation Test ===")
    test1(0)   # test3 (current)
    test1(-1)  # test2 (caller)
    test1(-2)  # test1 (caller's caller)
    test1(-3)  # __main__ (root)
    test1(1)   # First frame (root caller)
    test1(2)   # Second frame
