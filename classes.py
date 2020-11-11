from itertools import permutations
from typing import Dict, List
from collections import ChainMap
from math import factorial, prod


class Partitioning(List[int]):

    def n_alphabets(self):
        """Determine how many alphabets result from this partitioning."""
        return prod(factorial(p) for p in self)


class Alphabet(List[str]):

    def partition(self, partitioning: Partitioning):
        """Split the Alphabet into multiple partitions."""
        symbols = self
        for partition_ in partitioning:
            yield Alphabet(symbols[:partition_])
            symbols = symbols[partition_:]


class Key(Dict[str, str]):

    @staticmethod
    def new(keys: Alphabet, values: Alphabet):
        """Create a new Key using one Alphabet as keys and the other as values."""
        return Key({key: value for key, value in zip(keys, values)})

    def flipped(self):
        """Return a key, where the keys and values are flipped."""
        return Key({value: key for key, value in self.items()})

    def symbols_ref(self):
        """Return the symbol set used by the reference texts."""
        return Alphabet(self.keys())

    def symbols_enc(self):
        """Return the symbol set used by the encrypted texts."""
        return Alphabet(self.values())

    def permutations(self):
        """Generate every possible permutation of this key as a new Key."""
        for symbol_perm in permutations(self.symbols_enc()):
            yield Key.new(self.symbols_ref(), symbol_perm)

    def partition(self, partitioning: Partitioning):
        """Split the key into multiple partitions."""
        part_ref = self.symbols_ref().partition(partitioning)
        part_enc = self.symbols_enc().partition(partitioning)
        yield from (Key.new(ref, enc) for ref, enc in zip(part_ref, part_enc))

    def join(*keys):
        """Join multiple keys into a single one."""
        return Key(ChainMap(*keys))

    def compare(self, key):
        """Compare two Key-objects against each other."""
        return sum(self[k] == key[k] for k in self.keys()) / len(self.keys())


class Text(List[str]):

    @staticmethod
    def from_string(string: str, symbols: Alphabet, replace):
        """Create a new Text instance from a string."""
        string = string.lower()
        for old, new in replace.items():
            string = string.replace(old, new)
        return Text(c for c in string if c in symbols)

    @staticmethod
    def from_file(file: str, symbols: Alphabet, replace):
        """Create a new Text instance from a file."""
        with open(file, encoding="utf-8") as f:
            return Text.from_string(f.read(), symbols, replace)

    def encoded(self, key: Key):
        """Encode the text using mono-alphabetic substitution."""
        return Text([key[c] for c in self])

    def decoded(self, key: Key):
        """Decode the text using mono-alphabetic substitution."""
        return self.encoded(key.flipped())

    def frequencies(self, symbols: Alphabet):
        """Return the frequencies of the given symbols within the text."""
        return Frequencies({symbol: self.count(symbol) / len(self) for symbol in symbols})

    def compare(self, text):
        """Compare two Text-objects against each other."""
        return sum(char1 == char2 for char1, char2 in zip(self, text)) / len(self)

    def __str__(self):
        return str().join(self)


class Frequencies(Dict[str, float]):

    def sorted_symbols(self):
        """Return a Alphabet sorted after their frequency."""
        return Alphabet([i for i, value in sorted(self.items(), key=lambda x: x[1])])

    def encoded(self, key: Key):
        """Encode the frequencies using mono-alphabetic substitution.

        finding the frequencies of a text and then encoding the frequencies will have the same effect as first encoding
        the text and then finding the frequencies."""
        return Frequencies({key[c]: value for c, value in self.items()})

    def decoded(self, key):
        """Decode the frequencies using mono-alphabetic substitution.

        finding the frequencies of a text and then decoding the frequencies will have the same effect as first decoding
        the text and then finding the frequencies."""
        return self.encoded(key.flipped())
