import unittest
from nrc.util.window import *


class TestWindowManager(unittest.TestCase):
    def test_w_manager_init_and_add(self):
        train_sample_count = 10
        test_sample_count = 5
        data_buffer_size = 8

        wm = WindowManager(train_sample_count, test_sample_count, data_buffer_size)

        self.assertTrue(wm.is_pre_training)

        cnt = 0
        for i in range(1, 21):
            wm.add_one(i, i+1)
            cnt += 1
        print(cnt)

        print(f'Training sample count : {wm.train_sample_count}')
        self.assertFalse(wm.is_pre_training)
        self.assertFalse(wm.is_pre_testing)
        print(f'Pre-testing sample count : {wm.pre_test_sample_count}')


        self.assertEqual(train_sample_count, wm.train_sample_count)
        self.assertEqual(test_sample_count, wm.pre_test_sample_count)

if __name__ == '__main__':
    unittest.main()
