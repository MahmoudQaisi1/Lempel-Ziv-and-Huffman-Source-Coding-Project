'''
Project: Source Encoding techniques (Huffman + Lempel-Ziv)
Date: 1st July 2023
Done By:
Mahmoud Qaisi - 1190831
Omar Qattosh - 1180424
'''

import numpy as np
import math as math
import collections
import queue


# Symbols
symbols = ['a', 'b', 'c', 'd']
# Probabilities
p = [0.4, 0.3, 0.2, 0.1]

# Sequence length
sequence_length = 100

# Calculate the entropy
entropy = -np.sum([p_i * np.log2(p_i) for p_i in p])

print(f"The source entropy is: {entropy:.4f} bits/symbol")

def lz78_encode(sequence):
    dictionary = {'' : 0}  # Initialize dictionary with empty string
    s = ''  # Initialize string
    result = []  # Initialize result
    for c in sequence:
        sc = s + c
        if sc not in dictionary:
            result.append((dictionary[s], c))
            dictionary[sc] = len(dictionary)
            s = ''
        else:
            s = sc
    if s:
        result.append((dictionary[s], ''))
    print(dictionary)
    return result, dictionary

# Number of sequences
num_sequences = 5

# Total bits needed for all sequences
total_bits = 0

for _ in range(num_sequences):
    # Generate sequence
    sequence = ''.join(np.random.choice(symbols, p=p, size=sequence_length))
    print(sequence)
    # Get the encoded sequence and the dictionary of phrases
    encoded_sequence, phrase_dictionary = lz78_encode(sequence)

    # Calculate the number of bits needed to encode the sequence
    num_bits = 0
    for index, char in encoded_sequence:
        num_bits += math.ceil(math.log2(len(phrase_dictionary) + 1))  # Bits for index
        num_bits += 8  # Bits for ASCII character

    total_bits += num_bits

# Calculate and print the average number of bits needed to encode a sequence
average_bits = total_bits / num_sequences
print(f"The average number of bits needed to encode a sequence is: {average_bits}")

bits_per_symbol = average_bits/sequence_length
print(f"The number of bits per symbol is: {bits_per_symbol:.4f}")

compression_ratio = average_bits/(sequence_length*8) * 100
print(f"The compression ratio is : {compression_ratio:.4f}")



class Node:
    def __init__(self, frequency, symbol=None, left_node=None, right_node=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left_node = left_node
        self.right_node = right_node

    def __lt__(self, other):
        return self.frequency < other.frequency

    def get_codes(self, current_code='', codes={}):
        if self.symbol is not None:
            codes[self.symbol] = current_code
        else:
            self.left_node.get_codes(current_code + '0', codes)
            self.right_node.get_codes(current_code + '1', codes)
        return codes

# Symbols and probabilities
symbols = ['a', 'b', 'c', 'd']
probabilities = [0.4, 0.3, 0.2, 0.1]

# Construct priority queue
pq = queue.PriorityQueue()
for symbol, probability in zip(symbols, probabilities):
    pq.put(Node(frequency=probability, symbol=symbol))

# Build Huffman tree
while pq.qsize() > 1:
    left_node = pq.get()
    right_node = pq.get()
    merged_node = Node(frequency=left_node.frequency + right_node.frequency,
                       left_node=left_node,
                       right_node=right_node)
    pq.put(merged_node)

# Get Huffman codes from tree
huffman_tree = pq.get()
huffman_codes = huffman_tree.get_codes()

print(huffman_codes)
# Calculate the average number of bits per symbol
average_bits = sum(probabilities[i] * len(huffman_codes[symbol]) for i, symbol in enumerate(symbols))

print(f"The average number of bits per symbol is: {average_bits}")

# Calculate the total bits needed to encode the sequence
total_bits = sum(len(huffman_codes[symbol]) for symbol in sequence)
print(sequence)
print(f"The total number of bits needed to encode the sequence is: {total_bits}")

compression_ratio = total_bits/(sequence_length*8) * 100
print(f"The compression ratio is : {compression_ratio:.4f}")