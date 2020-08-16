from typing import Tuple

import yaml


def get_api_key(path: str) -> Tuple[str, str]:
    with open(path, 'r') as stream:
        try:
            d = yaml.safe_load(stream)
            return d['key'], d['secret']
        except yaml.YAMLError as exc:
            print(exc)
