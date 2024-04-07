#!/usr/bin/env python3
import argparse
import typing
import unicodedata_reader as ur
from range import Range


class AutoSpacing(object):

    def __init__(self) -> None:
        # Originally based on:
        # https://drafts.csswg.org/css-text-4/#text-spacing-classes
        ideographs = ur.Set()
        scripts = (('Han', 'Hani'), ('Tangut', 'Tang'),
                   ('Khitan_Small_Script', 'Kits'), ('Nushu', 'Nshu'),
                   ('Hiragana', 'Hira'), ('Katakana', 'Kana'), ('Bopomofo',
                                                                'Bopo'))
        for script, scx in scripts:
            ideographs |= ur.Set.scripts(script)
            ideographs |= ur.Set.script_extensions(scx)
        ideographs -= ur.Set.east_asian_width('H')
        ideographs -= ur.Set.general_category('P')
        non_modifier_symbols = ur.Set.general_category('S')
        non_modifier_symbols -= ur.Set.general_category('Sk')
        ideographs -= non_modifier_symbols
        ideographs -= ur.Set.general_category('No')
        ideographs.add(0x3013)  # GETA MARK

        letters_numerals = ur.Set()
        letters_numerals |= ur.Set.general_category('L')
        letters_numerals |= ur.Set.general_category('M')
        letters_numerals |= ur.Set.general_category('Nd')
        letters_numerals -= ur.Set.east_asian_width('F')
        letters_numerals -= ur.Set.east_asian_width('H')
        letters_numerals -= ur.Set.east_asian_width('W')
        letters_numerals -= ur.Set.scripts('Hangul')
        letters_numerals -= ur.Set.script_extensions('Hang')

        self.ideographs = ideographs
        self.letters_numerals = letters_numerals

    def value(self, ch: str) -> typing.Optional[str]:
        code = ord(ch)
        if code in self.ideographs:
            return 'W'
        if code in self.letters_numerals:
            return 'N'
        return None

    headers = """#
# The comments following the number sign "#" list the East_Asian_Width property
# value, followed by the Unicode character name or names.
#
# Code points that have the value O and the East_Asian_Width property value N or
# Na are omitted.
#
# @missing: 0000..10FFFF; O
"""

    def print(self, args: typing.Any) -> None:
        if not args.tsv:
            print(self.headers)
        east_asian_width = ur.UnicodeDataReader.default.east_asian_width()
        get_value = lambda ch: (self.value(ch), east_asian_width.value(ord(ch))
                                )
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
        parser.add_argument('-f',
                            '--clear-cache',
                            action='store_true',
                            help='Clear the Unicode data cache.')
        args = parser.parse_args()
        if args.clear_cache:
            ur.UnicodeDataCachedReader.clear_cache()
        spacing = AutoSpacing()
        spacing.print(args)


if __name__ == "__main__":
    AutoSpacing.main()
