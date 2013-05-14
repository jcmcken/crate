from crate.filters.core import Filter, BelongsToFilter
from crate._rpm import get_header, compare_versions

class RpmArchFilter(Filter):
    def transform(self, item):
        return get_header(item)['arch']

class RpmNameFilter(Filter):
    def transform(self, item):
        return get_header(item)['name']

class RpmLatestFilter(BelongsToFilter):
    def build_args(self, items):
        storage = {}

        for item in items:
            current_header = get_header(item)
            rpm_name = current_header['name']
    
            if rpm_name not in storage:
                storage[rpm_name] = (item, current_header)
            else:
                old_filename, old_header = storage[rpm_name]
                comparison = compare_versions(old_header, current_header) 
                if comparison > 0:
                    storage[rpm_name] = (item, current_header)

        self.args = [ v[0] for v in storage.values() ]

