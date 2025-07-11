"""
Test suite for FrameInfo functionality.
"""
from tests.base_test_class import BaseTestClass

# Assuming FrameInfo is defined in frame_info module
from frame_info import frame_info


class TestFrameInfo(BaseTestClass):
    """
    Test class for FrameInfo.
    """

    def test_should_return_frame_info(self):
        """
        Test the frame info functionality.
        """
        # Add your test logic here
        __frame = frame_info.get_frame_info(0)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_collect_frame_stack")

        __frame = frame_info.get_frame_info(-1)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "__get_frame")

        __frame = frame_info.get_frame_info(-2)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "get_frame_info")

        __frame = frame_info.get_frame_info(-3)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "test_should_return_frame_info")

    def test_should_return_frame_info_without_index(self):
        """
        Test the frame info functionality.
        """
        __frame = frame_info.get_frame_info()
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"],
                         "test_should_return_frame_info_without_index")
