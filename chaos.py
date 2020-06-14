import yaml
import logging
from pprint import pformat

class Chaos:
    def __init__(self, config_file):
        self.setup_logging()
        self.parse_config_file(config_file)
    
    def setup_logging(self, name=None):
        if not name: name=__name__
        self.logger = logging.getLogger(name)
        c_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.logger.setLevel(logging.DEBUG)
        c_handler.setFormatter(formatter)
        self.logger.addHandler(c_handler)

    def parse_file(self, filename):
        self.logger.info(f'Loading config file: {filename}')
        with open(filename, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def run(self):
        self.logger.info('Started run')
        self.logger.debug(f'Parsed config file \n{pformat(self.config)}')


