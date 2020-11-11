from classes import Partitioning, Key, Text, Alphabet, Frequencies
from typing import Iterable
from itertools import product


def decode_sort(enc: Text, symbols_enc: Alphabet, ref: Text, symbols_ref: Alphabet):
    """Evaluate the used encryption key by pairing the symbols up according to their frequency."""
    freq_enc = enc.frequencies(symbols_enc)
    freq_ref = ref.frequencies(symbols_ref)

    sort_enc = freq_enc.sorted_symbols()
    sort_ref = freq_ref.sorted_symbols()

    return Key.new(sort_ref, sort_enc)


def fitness(freq_1: Frequencies, freq_2: Frequencies, symbols: Alphabet):
    """Evaluate the fitness of the decoded or encoded frequencies."""
    return sum((freq_1[symbol] - freq_2[symbol]) ** 2 for symbol in symbols)


def fitness_fast(freq_1: Frequencies, freq_2: Frequencies, symbols: Alphabet):
    """Evaluate the fitness of the decoded or encoded frequencies."""
    return - sum(freq_1[symbol] * freq_2[symbol] for symbol in symbols)


def test_keys(enc: Text, symbols_enc: Alphabet, ref: Text, symbols_ref: Alphabet, keys: Iterable[Key]):
    """Yield the fitness of every key in the keys iterable."""
    freq_enc = enc.frequencies(symbols_enc)
    freq_ref = ref.frequencies(symbols_ref)

    for key in keys:
        fitness_ = fitness_fast(freq_ref.encoded(key), freq_enc, symbols_enc)
        yield key, fitness_


def decode_fitness(enc: Text, symbols_enc: Alphabet, ref: Text, symbols_ref: Alphabet):
    """Evaluate the best key by finding the one with the lowest fitness score of all possible permutations."""
    key = Key.new(symbols_ref, symbols_enc)
    keys = key.permutations()

    best_key, best_fitness = None, float('inf')
    for key, fitness_ in test_keys(enc, symbols_enc, ref, symbols_ref, keys):
        if fitness_ < best_fitness:
            best_key, best_fitness = key, fitness_
    return best_key


def decode_partition_slow(enc: Text, symbols_enc: Alphabet, ref: Text, symbols_ref: Alphabet, part: Partitioning):
    """Evaluate the best key by limiting the amount of possible keys trough partitioning to save time."""
    starting_key = decode_sort(enc, symbols_enc, ref, symbols_ref)
    keys_raw = product(*(partition.permutations() for partition in starting_key.partition(part)))
    keys = (Key.join(*key) for key in keys_raw)

    best_key, best_fitness = None, float('inf')
    for key, fitness_ in test_keys(enc, symbols_enc, ref, symbols_ref, keys):
        if fitness_ < best_fitness:
            best_key, best_fitness = key, fitness_
    return best_key


def decode_partition_fast(enc: Text, symbols_enc: Alphabet, ref: Text, symbols_ref: Alphabet, part: Partitioning):
    """Evaluate the best key by applying decode_fitness on smaller partitions of the alphabet to save time."""
    starting_key = decode_sort(enc, symbols_enc, ref, symbols_ref)

    key = Key()
    for partition in starting_key.partition(part):
        best_permutation = decode_fitness(enc, partition.symbols_enc(), ref, partition.symbols_ref())
        key = key.join(best_permutation)
    return key
