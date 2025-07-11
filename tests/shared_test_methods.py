"""
Shared test methods for Python Application Generator 3.10 Basic Structure
"""
import pathlib
from unittest.mock import patch
from loguru import logger as loguru_logger

from frame_info.generated import __core as core
from frame_info.generated.__core import logger_wrapper

import tests.generated.shared_test_methods as generated


def logger() -> logger_wrapper.LoggerWrapper:
    """
    Return logger for the shared test methods.

    Frame stack at this point is:
        -5 : _callTestMethod() (unittest TestCase method)
        -4 : caller of this logger()
        -3 : logger() (this function)
        -2 : __core.get_frame_info() (public function to have name and line number)
        -1 : __core.__get_frame() (private function to get frame)
         0 : __core._collect_frame_stack() (private function to collect frame stack)

    """
    frame_info = core.get_frame_info(-4)
    return logger_wrapper.logger(
        frame_info=frame_info
    )


def getenv(test, key):
    """Getenv for mocked environment"""
    if key == "GIM_APPLICATIONS_ROOTPATH":
        return test.workspace

    raise KeyError(f"Environment variable {key} not found.")


def set_up(test):
    """Set up the test environment"""
    generated.set_up(test)
    patcher = patch("os.getenv", side_effect=lambda key: getenv(test, key))
    patcher.start()
    test.addCleanup(patcher.stop)


def tear_down(test, to_be_removed):
    """Tear down the test environment"""
    if not to_be_removed:
        to_be_removed = []

    whitelist = [
        "workspace/testi2",
        "workspace/testi2/tests/extension/test_my_class3.py",
        "workspace/testi2/tests/generated/test_my_class3.py",
    ]

    # if any whitelisted matches blacklisted path true is returned and filter removes it
    whitelist: list = [pathlib.Path(filepath) for filepath in whitelist]
    skipped: list = list(
        filter(
            lambda blacklisted: any(
                map(
                    lambda whitelisted: whitelisted.is_relative_to(blacklisted),
                    whitelist,
                )
            ),
            to_be_removed,
        )
    )
    result = set(to_be_removed) - set(skipped)
    generated.tear_down(test, result)