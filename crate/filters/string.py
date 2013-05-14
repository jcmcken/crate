from crate.filters.core import Filter

class BelongsToFilter(Filter):
    def matches(self, item):
        return item in self.args

class RegexFilter(Filter):
    def preprocess_args(self):
        self.args = map(re.compile, self.args)

    def matches(self, item):
        for regex in self.args:
            if regex.search(item):
                return True
        return False
        
