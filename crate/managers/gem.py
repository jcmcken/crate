from crate.managers.file import FileManager
from crate.exc import SyncError
from crate.fs import files_in_dir
from crate.proc import run
import shutil
import os
import logging

LOG = logging.getLogger(__name__)

class GemManager(FileManager):
    def locate(self):
        sources = [ files_in_dir(i, suffix='gem') for i in self.sources ]
        return reduce(lambda x, y: x + y, sources)
    
    def build(self, destination):
        code, stdout, stderr = run('gem generate_index -d %s' % destination)
        LOG.debug(stdout)
        if stderr:
            LOG.error(stderr)
        if code != 0:
            raise SyncError('failed to create gem index')
