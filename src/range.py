from collections.abc import Callable
from collections.abc import Iterator
import sys
import typing
import unicodedata


def unicode_name(c: int) -> str:
    try:
        return unicodedata.name(chr(c))
    except Exception as err:
        print('ERROR: U+{1:04X}: {0}'.format(err, c), file=sys.stderr)
        return ''


class Range(object):

    def __init__(self, value: typing.Any, min: int, max: int) -> None:
        self.value = value
        self.min = min
        self.max = max
        self.comment = None

    def to_string(self) -> str:
        comment = self.comment
        if not comment:
            comment = self.name()
            if not comment:
                return '{0:14} ; {1}'.format(self.code(), self.value)
        return '{0:14} ; {1}  # {2}'.format(self.code(), self.value, comment)

    def code(self) -> str:
        if self.min == self.max:
            return '{0:04X}'.format(self.min)
        return '{0:04X}..{1:04X}'.format(self.min, self.max)

    def name(self) -> str:
        if self.min == self.max:
            return '{0}'.format(unicode_name(self.min))
        return '{0}..{1}'.format(unicode_name(self.min),
                                 unicode_name(self.max))

    @staticmethod
    def ranges(get_value: Callable[[str], typing.Any]) -> Iterator["Range"]:
        last_value = None
        min = 0
        for c in range(0, 0x110000):
            ch = chr(c)
            category = unicodedata.category(ch)
            if category == 'Cn':  # Skip "Unassigned" code points.
                if last_value:
                    yield Range(last_value, min, c - 1)
                last_value = None
                continue
            value = get_value(ch)
            if value == last_value:
                continue
            if last_value:
                yield Range(last_value, min, c - 1)
            last_value = value
            min = c
        if last_value:
            yield Range(last_value, min, c - 1)
