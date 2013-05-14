import os
import yaml
from crate.fs import files_from_dir

DEFAULT_REPOSD_DIR = '/etc/crate/repos.d'
REPOSD_DIR = os.environ.get('CRATE_REPOSD_DIR', DEFAULT_REPOSD_DIR)

def load_repo_configs():
    config_files = files_in_dir(REPOSD_DIR, suffix='yml')
    return [ yaml.load(open(f)) for f in config_files ]
