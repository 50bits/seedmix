import os
import random
import json
import calendar;
import time;

base_path = os.path.dirname(__file__)
system_random = random.SystemRandom()

shuffled_word_index_map = {}
index_word_map = {}
word_index_map = {}

current_time = calendar.timegm(time.gmtime())

def remove_line_breaks(list):
    size = len(list)
    for i in range(0, size):
        list[i] = list[i].replace("\n", "")

def secure_shuffle(list):
    size = len(list)
    for index1 in range(0, size):
        value1 = list[index1]
        index2 = system_random.randrange(0, size)
        value2 = list[index2]
        # exchange
        list[index1] = value2
        list[index2] = value1

def create_index_word_map(list):
    size = len(list)
    for i in range(0, size):
        shuffled_word_index_map[list[i]] = i + 1
        index_word_map[i + 1] = list[i]

def create_word_index_map(list):
    size = len(list)
    for i in range(0, size):
        word_index_map[list[i]] = shuffled_word_index_map[list[i]]

# load seed words file
# https://github.com/bitcoin/bips/tree/master/bip-0039
with open(base_path + "/english.txt", "r") as in_file:
    words_orig = in_file.readlines()

# clean-up entries
remove_line_breaks(words_orig)

words = words_orig.copy()

# shuffle word list
system_random.shuffle(words)
# shuffle again using own impl
secure_shuffle(words)

# create result maps
create_index_word_map(words)
create_word_index_map(words_orig.copy())

# test result maps
for i in range(1, 2048):
    if(word_index_map[index_word_map[i]] != i):
        print("Test failed for index: " + str(i))

# persist result maps
with open(base_path + "/english_mixed_" + str(current_time) + ".txt", "w") as out_file:
    out_file.write(json.dumps(word_index_map) + "\n\n\n")
    out_file.write(json.dumps(index_word_map))
