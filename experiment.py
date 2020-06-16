from time import sleep, time
import yaml
import subprocess
from pprint import pformat
import shutil
import kubernetes

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
    
    @property
    def is_initialized(self):
        kubernetes.config.load_kube_config()
        custom = kubernetes.client.CustomObjectsApi()
        try:
           obj = custom.get_namespaced_custom_object(name=self.config['name'], group='litmuschaos.io', version='v1alpha1', namespace='default', plural='chaosengines')
           return obj['status']['engineStatus']=='initialized'
        except kubernetes.client.rest.ApiException as _:
            return False

    @property
    def is_completed(self):
        kubernetes.config.load_kube_config()
        custom = kubernetes.client.CustomObjectsApi()
        try:
           obj = custom.get_namespaced_custom_object(name=self.config['name'], group='litmuschaos.io', version='v1alpha1', namespace='default', plural='chaosengines')
           return obj['status']['engineStatus']=='completed'
        except kubernetes.client.rest.ApiException as _:
            return False

    def run(self, aut):
        self.logger.info(f"Starting {self.config['name']}")
        url = self.make_temp_copy()
        kubectl_apply = subprocess.run(['kubectl', 'apply', '-f', url], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_apply.stdout.decode('utf-8')))
        
        for i in range(60):
            self.logger.info(f'Waiting for engine initialization ({i+1}/60)')
            if self.is_initialized: break
            sleep(1)
        self.logger.info('Engine initialized')
        for i in range(60):
            self.logger.info(f'Waiting for engine completion ({i+1}/60)')
            if self.is_completed: break
            sleep(5)
        self.logger.info(f"{self.config['name']} finished")
    
    def delete(self):
        self.logger.info(f"Deleting {self.config['name']}")
        kubectl_delete = subprocess.run(['kubectl', 'delete', '-f', self.location], stdout=subprocess.PIPE)
        self.logger.debug(pformat(kubectl_delete.stdout.decode('utf-8')))

        