from crate.filters.core import Filter
from crate.rpm import get_header

class RpmArchFilter(Filter):
    def transform(self, item):
        return get_header(item)['arch']

class RpmNameFilter(Filter):
    def transform(self, item):
        return get_header(item)['name']
