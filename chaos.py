import yaml
from pprint import pformat
from itertools import product
from datetime import datetime
import subprocess
from time import sleep

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
        self.start_time = datetime.now()
    

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
        
        total_time = 0
        experiment_results = []
        for aut in self.auts:
            tries = 0
            done = False
            while not done and tries<4:
                for experiment in self.experiments:
                    aut.install()
                    experiment.run(aut) 
                    experiment.delete()
                    aut.delete()
                    self.logger.info('Experiment verdict: {}'.format(experiment.verdict))
                    self.logger.info('Installing AUT took {}'.format(aut.install_duration))
                    self.logger.info('Experiment took {}'.format(experiment.duration))
                    if experiment.verdict == 'Pass':
                        experiment_results.append((str(aut), str(experiment), str(aut.install_duration), str(experiment.duration), str(experiment.verdict)))
                        done = True
                    else:
                        tries += 1
                    nodes = ['node1', 'node2', 'node3', 'node4']
                    subprocess.run(['helm', 'del', 'nsm', '--purge'])
                    sleep(10)
                    self.logger.info('Deleted nsm')
                    for node in nodes:
                        self.logger.info('Handling {}'.format(node))
                        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-o' ,'ConnectTimeout=10', '-o', 'BatchMode=yes', node, "crictl ps | grep nsm | awk '{print $1}' | xargs crictl stop; sudo rm -rf /var/lib/networkservicemesh/"])
                        sleep(10)
                    sleep(60)
                    subprocess.run(["helm", "install", "nsm/nsm", "--name=nsm", "--values=/users/nekkartu/cnf-testbed/examples/workload-infra/nsm-k8s/values.yaml"])
                    self.logger.info('Installed nsm')
                    sleep(60)
            if not done:
                break


                            



                    
        self.logger.info('Full experiment summary:')
        self.logger.info('AUT\tExperiment\tAUT Install Time\tExperiment time\tVerdict')
        for result in experiment_results:
            self.logger.info('{0}\t{1}\t{2}\t{3}\t{4}'.format(*result))
                
        elapsed_time = datetime.now() - self.start_time
        self.logger.info('Total elapsed time: {}'.format(elapsed_time))
        

