import pathlib
from dataclasses import dataclass

import yaml


@dataclass
class CollegeConfig:
    phone: str
    email: str


@dataclass
class AdminConfig:
    name: str
    email: str


@dataclass
class CeleryConfig:
    broker: str
    backend: str


@dataclass
class Config:
    secret_key: str
    silk: bool
    debug_toolbar: bool
    college: CollegeConfig
    admin: AdminConfig
    celery: CeleryConfig


def get_config(file: pathlib.Path) -> Config:
    with open(file) as f:
        raw_yaml = yaml.safe_load(f)
    return Config(
        secret_key=raw_yaml["secret_key"],
        silk=raw_yaml["silk"],
        debug_toolbar=raw_yaml["debug_toolbar"],
        college=CollegeConfig(**raw_yaml["college"]),
        admin=AdminConfig(**raw_yaml["admin"]),
        celery=CeleryConfig(**raw_yaml["celery"]),
    )
