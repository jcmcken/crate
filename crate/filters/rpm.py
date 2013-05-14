from crate.filters.core import Filter
from crate._rpm import get_header, compare_versions

class RpmArchFilter(Filter):
    def transform(self, item):
        return get_header(item)['arch']

class RpmNameFilter(Filter):
    def transform(self, item):
        return get_header(item)['name']
