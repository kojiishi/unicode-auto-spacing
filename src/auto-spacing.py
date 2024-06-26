#!/usr/bin/env python3
import argparse
import re
import typing
import unicodedata_reader as ur


class AutoSpacing(object):

    def __init__(self) -> None:
        ideographs = ur.Set()
        scripts = []
        scripts += [('Bopomofo', 'Bopo')]
        scripts += [('Han', 'Hani')]
        scripts += [('Hangul', 'Hang')]
        scripts += [('Hiragana', 'Hira')]
        scripts += [('Katakana', 'Kana')]
        scripts += [('Khitan_Small_Script', 'Kits')]
        scripts += [('Nushu', 'Nshu')]
        scripts += [('Tangut', 'Tang')]
        scripts += [('Yi', 'Yiii')]
        # For `ea=N|Na`, prioritize `sc` > `ea` > `scx`.
        # * U+02EA-02EB should be 'W'. Its `sc=Bopo`.
        # * U+A700-A707 should be `O`. Its `sc=Zyyy` and `scx=Hani|Latn`.
        # https://github.com/unicode-org/unicodetools/issues/768
        for script, scx in scripts:
            ideographs |= ur.Set.script_extensions(scx)
        ideographs -= ur.Set.east_asian_width('N', 'Na')
        for script, scx in scripts:
            ideographs |= ur.Set.scripts(script)
        ideographs -= ur.Set.east_asian_width('H')
        ideographs -= ur.Set.general_category('P', 'No')
        non_modifier_symbols = ur.Set.general_category('S')
        non_modifier_symbols -= ur.Set.general_category('Sk')
        ideographs -= non_modifier_symbols
        ideographs.add(0x3013)  # GETA MARK

        letters_numerals = ur.Set()
        letters_numerals |= ur.Set.general_category('L', 'M', 'Nd')
        letters_numerals -= ur.Set.east_asian_width('F', 'H', 'W')

        conditional = ur.Set()
        conditional |= ur.Set.general_category('Po')
        conditional -= ur.Set.east_asian_width('F', 'H', 'W')
        conditional.remove(0x0022)  # QUOTATION MARK
        conditional.remove(0x0027)  # APOSTROPHE
        conditional.remove(0x002A)  # ASTERISK
        conditional.remove(0x002F)  # SOLIDUS
        conditional.remove(0x00B7)  # MIDDLE DOT
        conditional.remove(0x2020)  # DAGGER
        conditional.remove(0x2021)  # DOUBLE DAGGER
        conditional.remove(0x2026)  # HORIZONTAL ELLIPSIS

        self.ideographs = ideographs
        self.letters_numerals = letters_numerals
        self.conditional = conditional

    def value(self, code: int) -> typing.Optional[str]:
        if code in self.ideographs:
            return 'W'
        if code in self.conditional:
            return 'C'
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
        if args.tsv:
            encodings = ['cp932', 'sjis_2004', 'cp936', 'cp949', 'cp950']
            print('\t'.join(['Unicode', 'AS', 'EA', 'sc', *encodings, 'Name']))
            sc_by_code = ur.UnicodeDataReader.default.scripts().to_dict()
        else:
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
                print_as_range = not name or name.endswith('-*') or re.search(
                    r'-[\dA-F]+$', name)
                if print_as_range:
                    row = [
                        code, value, eaw,
                        self.value_if_common(sc_by_code, entry),
                        *([''] * len(encodings)), name
                    ]
                    print('\t'.join(row))
                    continue
                for c in entry.range():
                    row = [ur.u_hex(c), value, eaw, sc_by_code.get(c, '')]
                    c_as_str = chr(c)
                    for enc in encodings:
                        row.append(ur.u_enc(c_as_str, enc))
                    row.append(name_by_code.get(c, ''))
                    print('\t'.join(row))
                continue
            print('{0:14} ; {1}  # {2:2}  {3}'.format(code, value, eaw,
                                                      name).rstrip())

    @staticmethod
    def value_if_common(dict: typing.Dict[int, str],
                        entry: ur.UnicodeDataEntry):
        value = dict.get(entry.min)
        if value is None:
            return ''
        for c in range(entry.min + 1, entry.max + 1):
            if value != dict.get(c):
                return ''
        return value

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
