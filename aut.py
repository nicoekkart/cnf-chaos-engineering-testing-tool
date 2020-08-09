import subprocess
from pprint import pformat
from datetime import datetime

from logger import logger

class AUT:
    def __init__(self, values, aut_config):
        self.logger = logger(__name__)
        self.values = values
        self.config = aut_config
        self.install_start_time = 0
        self.install_end_time = 0

    @property
    def include_list(self):
        return self.config['include_list']

    @property
    def install_duration(self):
        return self.install_end_time - self.install_start_time

    def install(self):
        self.logger.info(f"Running {self.config['chart']['name']} with values {self.values}")
        self.install_start_time = datetime.now()
        helm_install = subprocess.run(['helm', 'install', self.config['chart']['path'], 
            '--name', self.config['chart']['name'], 
            '--set', ','.join('='.join(i) for i in self.values),
            '--wait'], stdout=subprocess.PIPE)
        self.install_end_time = datetime.now()
        self.logger.debug(pformat(helm_install.stdout.decode('utf-8')))
        return helm_install.returncode==0

    def delete(self):
        self.logger.info(f"Deleting {self.config['chart']['name']}")
        helm_delete = subprocess.run(['helm', 'del', self.config['chart']['name'], '--purge'], stdout=subprocess.PIPE)
        

    @staticmethod
    def expand_value(value):
        if type(value[1])==str and '..' in value[1]:
            bounds = list(int(bound) for bound in value[1].split('..'))
            bounds[1] += 1
            return [[value[0], str(i)] for i in range(*bounds)]
        elif type(value[1])==str and ',' in value[1]:
            bounds = list(int(bound) for bound in value[1].split(','))
            return [[value[0], str(i)] for i in bounds]
        else:
            return [[value[0], str(value[1])]]

        
    def __str__(self):
        return '{} {}'.format(self.config['chart']['name'], self.values)


