import argparse
from icu import UnicodeSet
import typing
import unicodedata
from range import Range


class AutoSpacing(object):

    def __init__(self) -> None:
        # https://drafts.csswg.org/css-text-4/#text-spacing-classes
        ideographs = UnicodeSet()
        ideographs.addAll(UnicodeSet(r'[[:sc=Han:][:scx=Han:]]'))
        ideographs.addAll(UnicodeSet(r'[[:sc=Hira:][:scx=Hira:]-[:P:]]'))
        ideographs.addAll(UnicodeSet(r'[[:sc=Kana:][:scx=Kana:]-[:P:]]'))

        letters_numerals = UnicodeSet()
        letters_numerals.addAll(UnicodeSet(r'[[:L:][:M:][:Nd:]]'))
        letters_numerals.removeAll(UnicodeSet(r'[[:ea=F:]]'))

        self.ideographs = ideographs
        self.letters_numerals = letters_numerals

    def value(self, ch: str) -> typing.Optional[str]:
        if self.ideographs.contains(ch):
            return 'W'
        if self.letters_numerals.contains(ch):
            return 'N'
        return None

    headers = """#
# The comments following the number sign "#" list the East_Asian_Width property
# value, followed by the Unicode character name or names.
#
# @missing: 0000..10FFFF; O
"""

    def print(self, args: typing.Any) -> None:
        if not args.tsv:
            print(self.headers)
        get_value = lambda ch: (self.value(ch), unicodedata.east_asian_width(ch
                                                                             ))
        ranges = Range.ranges(get_value)
        for range in ranges:
            values = range.value
            value = values[0]
            eaw = values[1]
            if value is None:
                if eaw.startswith('N'):
                    continue
                value = 'O'
            range.value = value
            if args.tsv:
                print('\t'.join(
                    ('U' + range.code(), value, eaw, range.name())))
                continue
            print(
                range.to_string(
                    comment='{1:2}  {0}'.format(range.comment(), eaw)))

    @staticmethod
    def main() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--tsv', action='store_true')
        args = parser.parse_args()
        spacing = AutoSpacing()
        spacing.print(args)


if __name__ == "__main__":
    AutoSpacing.main()
