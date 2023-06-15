import os
from typing import Any
import yaml


class Context:

    def __init__(self):
        self.project_path: str = os.getcwd()

        configs = self.read_configs()
        self.db_config = configs['db']
        self.email_config = configs['email']
        self.secret_key = configs['secret_key']
        try:
            os.makedirs(os.path.join(self.project_path, 'media', 'excel'))
        except FileExistsError:
            pass

    def read_configs(self) -> dict[str, Any]:

        config_path = os.path.join(self.project_path, 'config.yaml')
        default_config = os.path.join(self.project_path, 'default_cfg.yaml')
        with open(default_config, 'r') as cfg:
            configs = yaml.safe_load(cfg)

        if os.path.exists(config_path):
            with open(config_path, 'r') as cfg:
                configs.update(yaml.safe_load(cfg) or {})
        else:
            with open(config_path, 'w') as cfg:
                yaml.dump(configs, cfg, default_flow_style=False)

        return configs


context = Context()
