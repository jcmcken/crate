from crate.managers.file import FileManager
from crate.fs import files_in_dir
from crate.proc import run
import shutil
import os
import logging

LOG = logging.getLogger(__name__)

class RpmManager(FileManager):
    def locate(self):
        sources = [ files_in_dir(i, suffix='rpm') for i in self.sources ]
        return reduce(lambda x, y: x + y, sources)
    
    def build(self, destination):
        code, stdout, stderr = run('createrepo -c .cache .', cwd=destination)
        LOG.debug(stdout)
        if stderr:
            LOG.error(stderr)

    def stage(self, files):
        tmpdir = FileManager.stage(self, files)

        # copy in old repodata and createrepo cache if they exist
        for d in 'repodata', '.cache':
            full = os.path.join(self.destination, d)
            if os.path.isdir(full):
                LOG.debug('copying "%s" directory to staged repo' % full)
                shutil.copytree(full, os.path.join(tmpdir, d))

        return tmpdir
