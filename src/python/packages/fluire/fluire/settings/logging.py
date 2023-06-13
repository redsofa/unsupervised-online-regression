import logging


logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO
                    )
logger.level = logging.DEBUG
logger.propagate = False

if __name__ == '__main__':
    pass
