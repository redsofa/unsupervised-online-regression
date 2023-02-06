from river import stream


class StreamFactory():

    @staticmethod
    def get_csv_stream(i_input_file, **i_kwargs):
        return stream.iter_csv(i_input_file, **i_kwargs)

    @staticmethod
    def get_kafka_stream(i_kafka_topic, i_bootstrap_servers, *i_kwargs):
        raise NotImplementedError('Not implemented yet.')


if __name__ == '__main__':
    pass
