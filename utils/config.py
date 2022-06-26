import pathlib
from dataclasses import dataclass

import yaml


@dataclass
class EnvConfig:
    debug: bool
    secret_key: str
    silk: bool
    debug_toolbar: bool


@dataclass
class CollegeConfig:
    phone: str
    email: str


@dataclass
class EmailSenderConfig:
    host: str
    port: int
    user: str
    password: str
    use_tls: bool


@dataclass
class AdminConfig:
    name: str
    email: str


@dataclass
class CeleryConfig:
    broker: str
    backend: str


@dataclass
class OAuth2GoogleConfig:
    client_id: str
    secret_key: str


@dataclass
class OAuth2Config:
    google: OAuth2GoogleConfig


@dataclass
class Config:
    env: EnvConfig
    college: CollegeConfig
    email_sender: EmailSenderConfig
    admin: AdminConfig
    celery: CeleryConfig
    oauth2: OAuth2Config


def get_config(file: pathlib.Path) -> Config:
    with open(file) as f:
        raw_yaml = yaml.safe_load(f)
    return Config(
        env=EnvConfig(**raw_yaml["env"]),
        college=CollegeConfig(**raw_yaml["college"]),
        admin=AdminConfig(**raw_yaml["admin"]),
        email_sender=EmailSenderConfig(**raw_yaml["email_sender"]),
        celery=CeleryConfig(**raw_yaml["celery"]),
        oauth2=OAuth2Config(**raw_yaml["oauth2"]),
    )
