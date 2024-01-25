from collections.abc import Iterator
from icu import UnicodeSet
import typing
from range import Range


class AutoSpacing(object):

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

    def ranges(self) -> Iterator[Range]:
        return Range.ranges(lambda ch: self.value(ch))

    headers = """#
# @missing: 0000..10FFFF; O
"""

    def print(self) -> None:
        print(self.headers)
        for range in self.ranges():
            print(range.to_string())

    @staticmethod
    def main() -> None:
        spacing = AutoSpacing()
        spacing.print()


if __name__ == "__main__":
    AutoSpacing.main()
