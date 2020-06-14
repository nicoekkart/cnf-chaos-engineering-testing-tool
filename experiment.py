from time import sleep

from logger import logger

class Experiment:
    def __init__(self):
        self.logger = logger(__name__)
        
    def run(self, aut):
        self.logger.info('Starting experiment...')
        sleep(5)
        self.logger.info('Experiment finished')
        