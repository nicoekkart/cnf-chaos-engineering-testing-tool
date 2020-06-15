import subprocess
from pprint import pformat

from logger import logger

class AUT:
    def __init__(self, values, aut_config):
        self.logger = logger(__name__)
        self.values = values
        self.config = aut_config

    @property
    def include_list(self):
        return self.config['include_list']

    def install(self):
        self.logger.info(f"Running {self.config['chart']['name']} with values {self.values}")
        helm_install = subprocess.run(['helm', 'install', self.config['chart']['path'], 
            '--name', self.config['chart']['name'], 
            #'--set', ','.join('='.join(i) for i in self.values),
            '--wait'], stdout=subprocess.PIPE)
        self.logger.debug(pformat(helm_install.stdout.decode('utf-8')))

    def delete(self):
        self.logger.info(f"Deleting {self.config['chart']['name']}")
        helm_delete = subprocess.run(['helm', 'del', self.config['chart']['name'], '--purge'], stdout=subprocess.PIPE)
        

    @staticmethod
    def expand_value(value):
        if type(value[1])==str and '..' in value[1]:
            bounds = list(int(bound) for bound in value[1].split('..'))
            bounds[1] += 1
            return [[value[0], str(i)] for i in range(*bounds)]
        else:
            return [[value[0], str(value[1])]]


