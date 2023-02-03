from river import stream


class StreamFactory():

    @staticmethod
    def get_csv_stream(input_file, target, **kwargs):
        return stream.iter_csv(input_file, **kwargs)

    @staticmethod
    def get_kafka_stream(kafka_topic, bootstrap_servers, *kwargs):
        raise NotImplementedError('Not implemented yet.')


if __name__ == '__main__':
    pass
