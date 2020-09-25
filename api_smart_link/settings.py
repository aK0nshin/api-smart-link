from dataclasses import asdict, dataclass
import threading

import uvloop
import asyncio

from databases import DatabaseURL

from api_smart_link.envmapping import BaseEnvMapping, EnvType, field

uvloop.install()
loop = asyncio.get_event_loop()

storage = threading.local()
storage.config = None


@dataclass(frozen=True)
class Settings(BaseEnvMapping):
    db_url: str = field(env_type=EnvType.string)
    listen_port: int = field(env_type=EnvType.int, default=8788)
    listen_host: str = field(env_type=EnvType.string, default='0.0.0.0')
    log_level: str = field(env_type=EnvType.string, default='WARNING')


def build_config():
    if storage.config:
        return storage.config
    settings = Settings.create()
    storage.config = settings
    return storage.config


def represent_conf():
    skip_suffixes = ['password', 'secret']
    return {
        key: value for key, value in asdict(storage.config).items()
        if all(key.find(skip) < 0 for skip in skip_suffixes)
    }
