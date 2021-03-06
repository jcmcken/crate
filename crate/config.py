import logging
import os
import yaml
from crate.fs import files_in_dir, expandpath
from crate.filters import FILTERS
from crate.managers import MANAGERS
from crate.exc import ConfigurationError, InvalidManager, InvalidFilter

DEFAULT_REPOSD_DIR = '/etc/crate/repos.d'
LOG_LEVELS = {
  'info': logging.INFO,
  'warn': logging.WARN,
  'error': logging.ERROR,
  'debug': logging.DEBUG,
  'fatal': logging.FATAL,
}

def load_repo_configs(directory):
    config_files = files_in_dir(directory, suffix='yml')
    configs = []
    for f in config_files:
        config = yaml.load(open(f))
        config['config_file'] = f
        configs.append(config)
    return configs

def load_filter(config):
    name = config.get('name', None)
    mode = config.get('mode', None)
    args = config.get('args', [])

    if not name:
        raise ConfigurationError('must specify filter name')

    filter = FILTERS.get(name, None)

    if not filter:
        raise InvalidFilter("no implementation for filter '%s'" % name)

    if mode:
        if mode not in filter.allowed_modes:
            raise InvalidFilter('invalid mode "%s", must be one of: %s' % (mode, filter.allowed_modes))
    else:
        mode = 'allow'

    filter = filter(name=name, mode=mode, args=args)

    return filter

def load_config(config):
    config_file = config.get('config_file', None)
    driver = config.get('driver', None)
    sources = config.get('sources', None)
    destination = config.get('destination', None)
    filters = config.get('filters', [])

    if None in [driver, sources, destination]:
        raise ConfigurationError('configurations must contain at least a '
                                 'driver, sources, and a destination.')

    destination = expandpath(destination)
    sources = map(expandpath, sources)

    manager = MANAGERS.get(driver, None)
    if not manager:
        raise InvalidManager('no implementation for manager "%s"' % driver)

    loaded_filters = [ load_filter(f) for f in filters ]

    manager = manager(config_file=config_file, sources=sources, destination=destination, 
        filters=loaded_filters)
    
    return manager 
    
