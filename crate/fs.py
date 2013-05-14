import os
import shutil
import tempfile
import logging
from crate.ui import confirm

LOG = logging.getLogger(__name__)

def files_in_dir(directory, suffix=None):
    directory = os.path.realpath(directory)
    LOG.debug('searching "%s" for files' % directory)
    try:
        root, dirs, files = os.walk(directory).next()
    except StopIteration:
        return []

    result = ( os.path.join(root, i) for i in files )
    if suffix:
        result = ( i for i in result if i.endswith('.' + suffix) )

    return list(result)

def safe_overwrite_dir(old, new, warn_on_overwrite=False):
    isdir = os.path.isdir(old)
    if isdir:
        if warn_on_overwrite:
            confirm('Destination directory "%s" exists, OK to overwrite?')
        tempdir = tempfile.mkdtemp()
        os.rmdir(tempdir)
        os.rename(old, tempdir)
        LOG.warn("the directory '%s' exists, moved to '%s' temporarily" % (old, tempdir))
    LOG.debug('moving staged repo "%s" to "%s"' % (new, old))
    os.rename(new, old)
    if isdir:
        LOG.warn("removing old directory and all of its contents")
        shutil.rmtree(tempdir)
