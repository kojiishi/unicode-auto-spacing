#!/usr/bin/env python3
import argparse
import typing
import unicodedata_reader as ur


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

    def value(self, code: int) -> typing.Optional[str]:
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
        code_points = range(0, 0x110000)

        # Make a list of pairs of (code, value).
        #
        # To make the AS list easy to compare with EA, the value is a tuple of
        # (AS, EA). Tuples will be merged only when both values are the same.
        eaw_by_code = ur.UnicodeDataReader.default.east_asian_width().to_dict()
        unassigned = ur.Set.general_category('Cn')  # "Unassigned"

        def to_pairs():
            for code in code_points:
                if code in unassigned:  # Skip unassigned code points.
                    continue
                yield (code, (self.value(code), eaw_by_code.get(code)))

        # Convert the list to a list of tuples of min, max, and value.
        entries = ur.UnicodeDataEntry.from_pairs(to_pairs())

        name_by_code = ur.UnicodeDataReader.default.name().to_dict()
        for entry in entries:
            # Restore the value from a tuple of (AS, EA).
            value, eaw = entry.value
            if value is None:
                if eaw.startswith('N'):
                    continue  # Omit printing `O` if `EA=N`.
                value = 'O'
            entry.value = value

            code = entry.range_as_str()
            name = entry.range_as_str(lambda c: name_by_code.get(c, ''))
            if args.tsv:
                print('\t'.join(('U' + code, value, eaw, name)))
                continue
            line = '{0:14} ; {1}  # {2:2}  {3}'.format(code, value, eaw,
                                                       name).rstrip()
            print(line)

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
