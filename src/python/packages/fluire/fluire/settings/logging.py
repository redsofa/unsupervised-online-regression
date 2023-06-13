import logging
import sys

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG
                    # level=logging.INFO
                    )
logger.propagate = False

if __name__ == '__main__':
    pass
