from crate.fs import safe_overwrite_dir
import logging

LOG = logging.getLogger(__name__)

class Manager(object):
    def __init__(self, name, sources, destination, filters=[]):
        self.name = name
        self.sources = sources
        self.destination = destination
        self.filters = filters

    def sync(self):
        files = self.locate()
        LOG.debug("located %d files" % len(files))
        filtered_files = self.filter(files)
        LOG.debug("filtered down to %d files" % len(filtered_files))
        temp_dest = self.stage(filtered_files)
        self.build(temp_dest)
        self.migrate(temp_dest)

    def locate(self):
        """
        Iterate over ``self.sources``, locating the appropriate file set that
        will be symlinked into ``self.destination``.

        Should return a list-like object.
        """
        raise NotImplementedError

    def filter(self, items):
        """
        Iterate over ``self.filters``, filtering out unwanted items.
        """
        return [ i for i in items for f in self.filters if f.filter(i) ]

    def stage(self, files):
        """
        Move filtered files from ``self.sources`` to ``self.destination``.
        """
        raise NotImplementedError

    def build(self, destination):
        """
        Action to perform on ``self.destination`` directory once appropriate files 
        are moved into place.
        """
        raise NotImplementedError

    def migrate(self, source):
        """
        Migrate the staged data to ``self.destination``.
        """
        raise NotImplementedError

