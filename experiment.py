from time import sleep, time
import yaml
import subprocess
from pprint import pformat
import shutil

from logger import logger

class Experiment:
    def __init__(self, config, conditions):
        self.logger = logger(__name__)
        self.config = config
        self.conditions = conditions
    
    def set_name(self, dir):
        with open(f'{dir}chaosengine.yaml', 'r') as f:
            y = yaml.load(f, Loader=yaml.FullLoader)
            y['metadata']['name'] = self.config['name']
        with open(f'{dir}chaosengine.yaml', 'w') as f:
            yaml.safe_dump(y, f)

    def make_temp_copy(self):
        dst = shutil.copytree(self.config['path'], f'.tmp/{int(time())}/')
        self.set_name(dst)
        self.location = dst
        return dst
        
    def run(self, aut):
        sleep(10)
        self.logger.info(f"Starting {self.config['name']}")
        url = self.make_temp_copy()
        # annotate the aut
        for d in aut.include_list:
            self.logger.info(f"Annotating {d['name']}")
            kubectl_annotate = subprocess.run(['kubectl', 'annotate', f"{d['type']}/{d['name']}", 'litmuschaos.io/chaos="true"'], stdout=subprocess.PIPE)
            self.logger.debug(pformat(kubectl_annotate.stdout.decode('utf-8')))
        kubectl_apply = subprocess.run(['kubectl', 'apply', '-f', self.config['path']], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_apply.stdout.decode('utf-8')))
        sleep(10)
        for d in aut.include_list:
            self.logger.info(f"Annotating {d['name']}")
            kubectl_annotate = subprocess.run(['kubectl', 'annotate', f"{d['type']}/{d['name']}", 'litmuschaos.io/chaos="false"', '--overwrite'], stdout=subprocess.PIPE)
            self.logger.debug(pformat(kubectl_annotate.stdout.decode('utf-8')))
        sleep(10)
        for d in aut.include_list:
            self.logger.info(f"Annotating {d['name']}")
            kubectl_annotate = subprocess.run(['kubectl', 'annotate', f"{d['type']}/{d['name']}", 'litmuschaos.io/chaos="true"', '--overwrite'], stdout=subprocess.PIPE)
            self.logger.debug(pformat(kubectl_annotate.stdout.decode('utf-8')))
        sleep(10)
        sleep(10)
        kubectl_apply = subprocess.run(['kubectl', 'delete', '-f', self.config['path']], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_apply.stdout.decode('utf-8')))
        sleep(10)
        kubectl_apply = subprocess.run(['kubectl', 'apply', '-f', self.config['path']], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_apply.stdout.decode('utf-8')))
        sleep(60)

        for d in aut.include_list:
            self.logger.info(f"Annotating {d['name']}")
            kubectl_annotate = subprocess.run(['kubectl', 'annotate', f"{d['type']}/{d['name']}", 'litmuschaos.io/chaos="false"', '--overwrite'], stdout=subprocess.PIPE)
            self.logger.debug(pformat(kubectl_annotate.stdout.decode('utf-8')))
        sleep(10)
        for d in aut.include_list:
            self.logger.info(f"Annotating {d['name']}")
            kubectl_annotate = subprocess.run(['kubectl', 'annotate', f"{d['type']}/{d['name']}", 'litmuschaos.io/chaos="true"', '--overwrite'], stdout=subprocess.PIPE)
            self.logger.debug(pformat(kubectl_annotate.stdout.decode('utf-8')))

        while True:
            sleep(1) 
        self.logger.info(f"{self.config['name']} finished")
    
    def delete(self):
        self.logger.info(f"Deleting {self.config['name']}")
        kubectl_delete = subprocess.run(['kubectl', 'delete', '-f', self.config['path']], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_delete.stdout.decode('utf-8')))

        