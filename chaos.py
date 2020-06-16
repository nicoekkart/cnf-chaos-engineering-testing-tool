import yaml
from pprint import pformat
from itertools import product

from aut import AUT
from experiment import Experiment
from logger import logger

class Chaos:
    def __init__(self, config_file):
        self.logger = logger(__name__)
        self.config = self.parse_config_file(config_file)
        self.auts = self.create_auts()
        self.logger.debug(self.auts)
        self.experiments = self.create_experiments()
    

    def parse_config_file(self, filename):
        """
        Parses the yaml config file and loads it in self.config
        """
        self.logger.info(f'Loading config file: {filename}')
        with open(filename, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def create_auts(self):
        """
        Creates all possible AUTs from configuration and returns them
        """
        self.logger.info('Creating AUTs')
        values = list(map(AUT.expand_value, self.config['aut']['values'].items()))
        self.logger.debug(values)
        return [AUT(configuration, self.config['aut']) for configuration in product(*values)]
             
    def create_experiments(self):
        """
        Creates all possible experiments from configuration and returns them
        """
        self.logger.info('Creating experiments')
        return [Experiment(exp_conf, self.config['conditions']) for exp_conf in self.config['experiments']]

    def run(self):
        self.logger.info(f"Started {self.config['name']}")
        self.logger.debug(f'Parsed config file \n{pformat(self.config)}')
        
        for aut in self.auts:
            for experiment in self.experiments:
                aut.install()
                experiment.run(aut) 
                experiment.delete() 
                aut.delete()

