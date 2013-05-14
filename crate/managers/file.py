from crate.managers.core import Manager
from crate.fs import files_in_dir, safe_overwrite_dir
import os
import tempfile
import logging

LOG = logging.getLogger(__name__)

class FileManager(Manager):
    def locate(self):
        sources = [ files_in_dir(i) for i in self.sources ]
        return reduce(lambda x, y: x + y, sources)

    def stage(self, files):
        tmpdir = tempfile.mkdtemp()
        LOG.debug('staging directory is "%s"' % tmpdir)
        for f in files:
            fname = os.path.basename(f)
            full = os.path.join(tmpdir, fname)
            LOG.debug('staging file "%s" at "%s"' % (f, full))
            os.symlink(f, full)
        return tmpdir

    def build(self, destination):
        """
        Nothing to do, we're just symlinking a bunch of files
        """
        pass

    def migrate(self, source):
        safe_overwrite_dir(self.destination, source)
