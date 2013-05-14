from crate.managers.file import FileManager
from crate.fs import files_in_dir
from crate.proc import run

class RpmManager(FileManager):
    def locate(self):
        sources = [ files_in_dir(i, suffix='rpm') for i in self.sources ]
        return reduce(lambda x, y: x + y, sources)
    
    def build(self, destination):
        code, stdout, stderr = run('createrepo -c .cache .', cwd=destination)
