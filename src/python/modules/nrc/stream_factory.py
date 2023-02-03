from river import stream


class StreamFactory():

    @staticmethod
    def get_csv_stream(input_file, target, **kwargs):
        return stream.iter_csv(input_file, **kwargs)


if __name__ == '__main__':
    pass
