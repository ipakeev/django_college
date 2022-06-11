import pathlib
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    secret_key: str
    silk: bool
    debug_toolbar: bool


def get_config(file: pathlib.Path) -> Config:
    with open(file) as f:
        raw_yaml = yaml.safe_load(f)
    return Config(
        secret_key=raw_yaml["secret_key"],
        silk=raw_yaml["silk"],
        debug_toolbar=raw_yaml["debug_toolbar"],
    )
