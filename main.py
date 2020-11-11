from classes import Alphabet, Text, Partitioning, Key
from program import decode_partition_fast, fitness, decode_partition_slow, decode_sort, decode_fitness

# Example SymbolSets
SymbolSets = {
    "Standard": Alphabet([*"abcdefghijklmnopqrstuvwxyz"]),
    "Reversed": Alphabet([*"zyxwvutsrqponmlkjihgfedcba"]),
    "Symbols": Alphabet([*"!§$%&/()=?-_{[]}#'+~:;.,@<"]),

    "Standard27": Alphabet([*"abcdefghijklmnopqrstuvwxyz "]),
    "Reversed27": Alphabet([*" zyxwvutsrqponmlkjihgfedcba"]),
    "Symbols27": Alphabet([*"!§$%&/()=?-_{[]}#'+~:;.,@<|"])
}
# Example Partitionings
Partitioning_ = {
    "Slow": Partitioning((6, 10, 9, 1)),
    "Normal": Partitioning((4, 2, 5, 5, 3, 5, 1, 1)),
    "Fast": Partitioning((4, 2, 5, 2, 3, 3, 3, 2, 1, 1)),

    "Slow27": Partitioning((6, 10, 9, 1, 1)),
    "Normal27": Partitioning((4, 2, 5, 5, 3, 5, 1, 1, 1)),
    "Fast27": Partitioning((4, 2, 5, 2, 3, 3, 3, 2, 1, 1, 1))
}
replace = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}

# Choosing the SymbolSets and the Partitioning
symbols_ref = SymbolSets["Standard"]
symbols_enc = SymbolSets["Reversed"]
partitioning = Partitioning_["Fast"]

# Creating the encryption key
key = Key.new(symbols_ref, symbols_enc)

# Loading the included text files
sandmann = Text.from_file("sandmann.txt", symbols_ref, replace)
winnetou = Text.from_file("Winnetou.txt", symbols_ref, replace)
perfect26 = Text.from_file("perfect_reference26.txt", symbols_ref, replace)

# Encoding the included text files
sandmann_enc = sandmann.encoded(key)
winnetou_enc = winnetou.encoded(key)

# Choosing encrypted text and reference text
text_enc = sandmann_enc
text_ref = perfect26

if __name__ == "__main__":
    keys = {'comp_key1': decode_sort(text_enc, symbols_enc, text_ref, symbols_ref),
            # 'comp_key2': decode_fitness(text_enc, symbols_enc, text_ref, symbols_ref),
            'comp_key3': decode_partition_slow(text_enc, symbols_enc, text_ref, symbols_ref, partitioning),
            'comp_key4': decode_partition_fast(text_enc, symbols_enc, text_ref, symbols_ref, partitioning)}

    texts = {'true_dec': text_enc.decoded(key),
             'comp_dec1': text_enc.decoded(keys['comp_key1']),
             # 'comp_dec2': text_enc.decoded(keys['comp_key2']),
             'comp_dec3': text_enc.decoded(keys['comp_key3']),
             'comp_dec4': text_enc.decoded(keys['comp_key4'])}

    freqs = {'ref_freq': text_ref.frequencies(symbols_ref),
             'true_freq': texts['true_dec'].frequencies(symbols_ref),
             'comp_freq1': texts['comp_dec1'].frequencies(symbols_ref),
             # 'comp_freq2': texts['comp_dec2'].frequencies(symbols_ref),
             'comp_freq3': texts['comp_dec3'].frequencies(symbols_ref),
             'comp_freq4': texts['comp_dec4'].frequencies(symbols_ref)}

    fitness_ = {'true_fit': fitness(freqs['ref_freq'], freqs['true_freq'], symbols_ref),
                'comp_fit1': fitness(freqs['ref_freq'], freqs['comp_freq1'], symbols_ref),
                # 'comp_fit2': fitness(freqs['ref_freq'], freqs['comp_freq2'], symbols_ref),
                'comp_fit3': fitness(freqs['ref_freq'], freqs['comp_freq3'], symbols_ref),
                'comp_fit4': fitness(freqs['ref_freq'], freqs['comp_freq4'], symbols_ref)}

    text_acc = {'comp_acc_t1': texts['true_dec'].compare(texts['comp_dec1']),
                # 'comp_acc_t2': texts['true_dec'].compare(texts['comp_dec2']),
                'comp_acc_t3': texts['true_dec'].compare(texts['comp_dec3']),
                'comp_acc_t4': texts['true_dec'].compare(texts['comp_dec4'])}

    key_acc = {'comp_acc_k1': key.compare(keys['comp_key1']),
               # 'comp_acc_k2': key.compare(keys['comp_key2']),
               'comp_acc_k3': key.compare(keys['comp_key3']),
               'comp_acc_k4': key.compare(keys['comp_key4'])}

    print('fitness:\n'
          '\n'
          '\ttrue fitness:\t\t{true_fit}\n'
          '\tdecode sort:\t\t{comp_fit1}\n'
          # '\tdecode fitness:\t\t{comp_fit2}\n'
          '\tdecode partition slow:\t{comp_fit3}\n'
          '\tdecode partition fast:\t{comp_fit4}\n'
          '\n'
          'text accuracy:\n'
          '\n'
          '\tdecode sort:\t\t{comp_acc_t1}\n'
          # '\tdecode fitness:\t\t{comp_acc_t2}\n'
          '\tdecode partition slow:\t{comp_acc_t3}\n'
          '\tdecode partition fast:\t{comp_acc_t4}\n'
          '\n'
          'key accuracy:\n'
          '\n'
          '\tdecode sort:\t\t{comp_acc_k1}\n'
          # '\tdecode fitness:\t\t{comp_acc_k2}\n'
          '\tdecode partition slow:\t{comp_acc_k3}\n'
          '\tdecode partition fast:\t{comp_acc_k4}\n'
          '\n'.format(**fitness_, **text_acc, **key_acc))

    print(Text(texts['comp_dec1'][:1000]))

    input('press ENTER to exit.')
