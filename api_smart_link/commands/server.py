import click

from api_smart_link.commands import cli
from api_smart_link.settings import build_config


@cli.group()
def server():
    pass


@server.command('run')
@click.option('--log_level', default=None, show_default=True, help='Log level')
def server_run(log_level: str = None):
    build_config()
    from api_smart_link.log_manager import log_manager
    log_manager.set_base_level(log_level.upper() if isinstance(log_level, str) else log_level)
    from api_smart_link.app import run
    run()
