from crate.filters.core import BelongsToFilter, RegexFilter
from crate.filters.rpm import (
  RpmNameFilter, RpmArchFilter, RpmLatestFilter, RpmNameRegexFilter,
)

FILTERS = {
  'regex': RegexFilter,
  'belongs_to': BelongsToFilter,
  'rpm_name': RpmNameFilter,
  'rpm_arch': RpmArchFilter,
  'rpm_latest': RpmLatestFilter,
  'rpm_name_regex': RpmNameRegexFilter,
}

