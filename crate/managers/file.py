from crate.managers.core import Manager
from crate.fs import files_in_dir, safe_overwrite_dir
import os
import tempfile
import logging
import datetime
import yaml

LOG = logging.getLogger(__name__)

class FileManager(Manager):
    def locate(self):
        sources = [ files_in_dir(i) for i in self.sources ]
        return reduce(lambda x, y: x + y, sources)

    def mark_repo(self, directory, files):
        crate_file = os.path.join(directory, '.crate')
        timestamp = str(datetime.datetime.now())
        try:
            generated_by = os.getlogin()
        except:
            generated_by = '<system>'
        config = yaml.load(open(self.config_file))
        tmpfile = crate_file + '.tmp'
        open(tmpfile, 'a').close()
        tmpfile_fd = open(tmpfile, 'w')
        data = yaml.dump({
            'timestamp': timestamp,
            'generated_by': generated_by,
            'config': config,
            'files': files,
        }, tmpfile_fd, explicit_start=True)
        os.rename(tmpfile, crate_file)

    def stage(self, files):
        tmpdir = tempfile.mkdtemp()
        self.mark_repo(tmpdir, files)
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
