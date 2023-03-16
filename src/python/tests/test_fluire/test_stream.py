from nrc.factories.stream import StreamFactory
import unittest
import io


class TestCSVStream(unittest.TestCase):
    def test_io(self):
        # A stub stream with 2 samples
        test_data = io.StringIO("c1,c2,t\n1,2,0\n3,2,1")
        params = {"converters": {"c1": float, "c2": float, 't': int}, "target": "t"}
        data_stream = StreamFactory.get_csv_stream(test_data, **params)
        cnt = 0
        for x, y in data_stream:
            cnt += 1

        self.assertTrue(cnt == 2)
        self.assertEqual(1, y)
        self.assertTrue(x['c1'] == 3.0)


if __name__ == '__main__':
    unittest.main()
