from collections.abc import Callable
from collections.abc import Iterator
import sys
import typing
import unicodedata
import unicodedata_reader as ur


def unicode_name(c: int) -> str:
    try:
        return unicodedata.name(chr(c))
    except Exception as err:
        print('ERROR: U+{1:04X}: {0}'.format(err, c), file=sys.stderr)
        return ''


class Range(object):

    unassigned = ur.Set.general_category('Cn')  # "Unassigned"

    def __init__(self, value: typing.Any, min: int, max: int) -> None:
        self.value = value
        self.min = min
        self.max = max

    def to_string(self, comment: typing.Optional[str] = None) -> str:
        output = '{0:14} ; {1}'.format(self.code(), self.value)
        if not comment:
            comment = self.comment()
        if comment:
            output = '{0}  # {1}'.format(output, comment)
        return output

    def code(self) -> str:
        if self.min == self.max:
            return '{0:04X}'.format(self.min)
        return '{0:04X}..{1:04X}'.format(self.min, self.max)

    def comment(self) -> str:
        return self.name()

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
            if c in Range.unassigned:  # Skip "Unassigned" code points.
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
