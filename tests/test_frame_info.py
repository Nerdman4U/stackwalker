"""
Test suite for FrameInfo functionality.
"""
import unittest

# Assuming FrameInfo is defined in frame_info module
from frame_info import frame_info


class TestFrameInfo(unittest.TestCase):
    """
    Test class for FrameInfo.
    """

    def test_get_frame_by_index(self):
        """
        Test the frame info functionality.
        """
        # Add your test logic here
        __frame = frame_info.get_frame_by_index(0)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_collect_frame_stack")

        __frame = frame_info.get_frame_by_index(-1)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_get_frame")

        __frame = frame_info.get_frame_by_index(-2)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "get_frame_by_index")

        __frame = frame_info.get_frame_by_index(-3)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "test_get_frame_by_index")

    def test_get_frame_by_name(self):
        """
        Test finding a frame by its name.
        """
        __frame = frame_info.get_frame_by_name(
            caller_name="_collect_frame_stack",
            module_name="frame_info.frame_info",
            offset=0
        )
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_collect_frame_stack")
        self.assertEqual(__frame["module_name"], "frame_info.frame_info")

    def test_should_return_frame_list(self):
        """
        Test the frame list functionality.
        """
        __frame_list = frame_info.get_frame_list()
        self.assertTrue(__frame_list)
        self.assertGreater(len(__frame_list), 0)

        # Check if the first frame is the current function
        self.assertEqual(__frame_list[0]["caller_name"],
                         "_collect_frame_stack")

    def test_should_return_frame_name_list(self):
        """
        Test the frame name list functionality.
        """
        __frame_name_list = frame_info.get_frame_name_list()
        self.assertTrue(__frame_name_list)
        self.assertGreater(len(__frame_name_list), 0)

        # import pprint
        # pprint.pprint(__frame_name_list[0:3])

        self.assertEqual(
            __frame_name_list[0], ("frame_info.frame_info", "_collect_frame_stack"))
        self.assertEqual(
            __frame_name_list[1], ("frame_info.frame_info", "get_frame_name_list"))
        self.assertTrue(
            __frame_name_list[2][0].endswith("test_frame_info")
        )
        self.assertEqual(
            __frame_name_list[2][1],
            "test_should_return_frame_name_list"
        )
