from crate.filters.rpm import RpmNameFilter, RpmArchFilter
from crate.filters.core import BelongsToFilter, RegexFilter

FILTERS = {
  'regex': RegexFilter,
  'belongs_to': BelongsToFilter,
  'rpm_name': RpmNameFilter,
  'rpm_arch': RpmArchFilter,
}

