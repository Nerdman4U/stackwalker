"""
Test suite for Stackwalker functionality.
"""
import unittest

from stackwalker import stackwalker


class TestStackwalker(unittest.TestCase):
    """
    Test class for Stackwalker.
    """

    def test_get_frame_by_index(self):
        """
        Test the frame info functionality.
        """
        # Add your test logic here
        __frame = stackwalker.get_frame_by_index(0)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_collect_frame_stack")

        __frame = stackwalker.get_frame_by_index(-1)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_get_frame")

        __frame = stackwalker.get_frame_by_index(-2)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "get_frame_by_index")

        __frame = stackwalker.get_frame_by_index(-3)
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "test_get_frame_by_index")

    def test_get_frame_by_name(self):
        """
        Test finding a frame by its name.
        """
        __frame = stackwalker.get_frame_by_name(
            caller_name="_collect_frame_stack",
            module_name="stackwalker.stackwalker",
            offset=0
        )
        self.assertTrue(__frame)
        self.assertEqual(__frame["caller_name"], "_collect_frame_stack")
        self.assertEqual(__frame["module_name"], "stackwalker.stackwalker")

    def test_should_return_frame_list(self):
        """
        Test the frame list functionality.
        """
        __frame_list = stackwalker.get_frame_list()
        self.assertTrue(__frame_list)
        self.assertGreater(len(__frame_list), 0)

        # Check if the first frame is the current function
        self.assertEqual(__frame_list[0]["caller_name"],
                         "_collect_frame_stack")

    def test_should_return_frame_name_list(self):
        """
        Test the frame name list functionality.

        python -m unittest: returns module name with package name e.g. stackwalker.stackwalker
        pytest: returns module name without package name e.g. stackwalker
        """
        __frame_name_list = stackwalker.get_frame_name_list()
        self.assertTrue(__frame_name_list)
        self.assertGreater(len(__frame_name_list), 0)

        # import pprint
        # pprint.pprint(__frame_name_list[0:3])

        self.assertEqual(
            __frame_name_list[0], ("stackwalker.stackwalker", "_collect_frame_stack"))
        self.assertEqual(
            __frame_name_list[1], ("stackwalker.stackwalker", "get_frame_name_list"))
        self.assertTrue(
            __frame_name_list[2][0].endswith("test_stackwalker")
        )
        self.assertEqual(
            __frame_name_list[2][1],
            "test_should_return_frame_name_list"
        )
