import io
from nrc.factories.stream import StreamFactory
import numpy as np

# Common unit test helper functions
def get_test_data_stream():
    def get_test_data():
        sample_data = \
                '''c1,c2,y
                1.0,2.0,23
                2.2,3.5,22
                3.0,3.1,21
                2.0,3.1,20
                2.4,3.4,22
                2.0,3.1,24
                6.0,3.1,26
                2.0,3.1,22
                4.2,3.1,22
                2.0,3.5,27
                2.1,3.1,None
                2.0,3.1,None
                2.4,3.2,None
                3.0,3.4,None
                1.0,2.0,None
                2.2,3.5,None
                3.0,3.1,None
                2.0,3.1,None
                2.4,3.4,None
                2.4,3.4,None
                2.4,3.4,None
                2.0,3.2,None
                '''.replace(' ', '')

        ret_val = io.StringIO(sample_data)
        return ret_val

    def  int_or_none(val):
        try :
            return int(val)
        except:
            return None

    def get_stream_params():
        return {"converters":{"c1":float, "c2":float, 'y':int_or_none}, "target":"y"}

    test_data = get_test_data()
    params = get_stream_params()
    data_stream = StreamFactory.get_csv_stream(test_data, **params)
    return data_stream


if __name__ == '__main__':
    pass
