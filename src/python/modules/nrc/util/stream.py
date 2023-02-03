import json


def load_stream_params(i_params_file):
    with open(i_params_file) as f:
        data = f.read()
    stream_params = json.loads(data)
    for e in stream_params['converters']:
        data_type = stream_params['converters'][e]
        if data_type == 'float':
            stream_params['converters'][e] = float
        elif data_type == 'int':
            stream_params['converters'][e] = int
        else:
            stream_params['converters'][e] = str
    return stream_params


if __name__ == '__main__':
    pass
