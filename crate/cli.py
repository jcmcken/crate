import sys
import optparse
import logging
from crate.config import (
    load_repo_configs, load_config, DEFAULT_REPOSD_DIR, LOG_LEVELS
)
from crate.managers import duplicate_destinations

LOG = logging.getLogger(__name__)

def get_cli():
    cli = optparse.OptionParser(
        usage='usage: crate [options]'
    )  
    cli.add_option('-c', '--config-dir', default=DEFAULT_REPOSD_DIR,
        help='Crate repos.d directory (defaults to "%s")' % DEFAULT_REPOSD_DIR)
    cli.add_option('-n', '--noop', action='store_true',
        help="Load configs, but don't sync any files")
    cli.add_option('-l', '--log-level', default='info', choices=LOG_LEVELS.keys(),
        help='Specify command-line logging verbosity')
    return cli

def main(argv=None):
    cli = get_cli()
    opts, args = cli.parse_args()

    LOG.root.setLevel(LOG_LEVELS[opts.log_level])
    LOG.debug('logging level set to "%s"' % opts.log_level)
    LOG.debug('config directory set to "%s"' % opts.config_dir)

    configs = load_repo_configs(opts.config_dir)
    managers = [ load_config(c) for c in configs ]

    if duplicate_destinations(managers):
        pass

    LOG.debug('loaded %d resource managers' % len(managers))

    if opts.noop:
        LOG.debug('noop is enabled, exiting')
        raise SystemExit

    LOG.info('beginning resource sync')
    for m in managers:
        LOG.info('syncing manager from "%s" (%s)' % (m.config_file, m.__class__.__name__))
        m.sync()

if __name__ == '__main__':
    main()
