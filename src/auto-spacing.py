from collections.abc import Iterator
from icu import UnicodeSet
import sys
import typing
import unicodedata


def unicode_name(c: int) -> str:
    try:
        return unicodedata.name(chr(c))
    except Exception as err:
        print('ERROR: U+{1:04X}: {0}'.format(err, c), file=sys.stderr)
        return ''


class EastAsianSpacing(object):

    def __init__(self) -> None:
        # https://drafts.csswg.org/css-text-4/#text-spacing-classes
        ideographs = UnicodeSet(
            r'[[\u3041-\u30FF]-[:P:][\u31C0-\u31FF][:sc=Han:]]')
        letters_numerals = UnicodeSet(r'[[:L:][:M:][:Nd:]-[:ea=F:]]')
        self.ideographs = ideographs
        self.letters_numerals = letters_numerals

    def value(self, ch: str) -> typing.Optional[str]:
        if self.ideographs.contains(ch):
            return 'W'
        if self.letters_numerals.contains(ch):
            return 'N'
        return None

    class Range(object):

        def __init__(self, value: str, min: int, max: int) -> None:
            self.value = value
            self.min = min
            self.max = max

        def format(self) -> str:
            comments = []
            if self.min == self.max:
                range = '{0:04X}'.format(self.min)
                comments.append('{0}'.format(unicode_name(self.min)))
            else:
                range = '{0:04X}..{1:04X}'.format(self.min, self.max)
                comments.append('{0}..{1}'.format(unicode_name(self.min),
                                                  unicode_name(self.max)))
            comment = '  # {0}'.format(' '.join(comments))
            return '{0:14} ; {1}{2}'.format(range, self.value, comment)

    def ranges(self) -> Iterator[Range]:
        last_value = None
        min = 0
        for c in range(0, 0x110000):
            ch = chr(c)
            category = unicodedata.category(ch)
            if category == 'Cn':  # Skip "Unassigned" code points.
                if last_value:
                    yield self.Range(last_value, min, c - 1)
                last_value = None
                continue
            value = self.value(ch)
            if value == last_value:
                continue
            if last_value:
                yield self.Range(last_value, min, c - 1)
            last_value = value
            min = c
        if last_value:
            yield self.Range(last_value, min, c - 1)

    headers = """#
# @missing: 0000..10FFFF; O
"""

    def print(self) -> None:
        print(self.headers)
        for range in self.ranges():
            print(range.format())

    @staticmethod
    def main() -> None:
        spacing = EastAsianSpacing()
        spacing.print()


if __name__ == "__main__":
    EastAsianSpacing.main()
