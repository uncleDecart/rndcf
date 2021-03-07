#!/usr/bin/python3

from collections import Counter
import itertools
import random
import re
import sys

if '--help' in str(sys.argv):
    print("""
Random coffee pair generator.
Options:
--dry-run will not add generated pairs to the file 
""")
    exit(0)

dry_run = True
if '--dry-run' in str(sys.argv):
    dry_run = True

names = set()
try:
    with open('names.txt', 'r') as fp:
        for line in fp:
            names.add(line.strip())
except:
    raise ValueError("could not find file names.txt")

past_pairs = []
try:
    with open('prev_pairs.txt', 'r') as fp:
        for line in fp:
            past_pairs.append(tuple([el[1:-1] for el in re.findall(r"\".*?\"", line.strip())]))
except:
    print("[Warning] Could not find file prev_pairs assuming there\'re no previous pairs") 

unique_pairs_counter = Counter([tuple(sorted(elem)) for elem in past_pairs])
print("Total pairs {}, unique_pairs {}".format(len(past_pairs), len(unique_pairs_counter)))

res = []
used_names = set()
possible_pairs = set([tuple(sorted(elem)) for elem in itertools.combinations(names,2)]) - set(past_pairs)

pairs_count = len(names) // 2

possible_pairs = list(possible_pairs)

for i in range(pairs_count):
    is_ppl_unique = False
    while not is_ppl_unique:
        pair = random.choice(possible_pairs)
        is_ppl_unique = pair[0] not in used_names and pair[1] not in used_names

    used_names.add(pair[0])
    used_names.add(pair[1])

    res.append(pair);

if len(res) < pairs_count: # we have iterated over all possible unique pairs for some people
    print("[Warning] We iterated over all possible unique pairs for some people")
    remain_names = names - used_names
    for i in range(len(remain_names//2)):
        first_name = random.sample(remain_names, 1)[0]
        remain_names.remove(el)
        second_name = random.sample(remain_names, 1)[0]
        remain_names.remove(el)

        res.append(tuple(first_name, second_name))
        used_names.add(first_name)
        used_names.add(second_name)
   
if len(names) % 2 == 1: # not odd we have triplet
    res[-1] += tuple(names - used_names)

print("Random coffee pairs are:")
i = 1
for pair in res:
    print("{}. {}".format(i, ' '.join(pair)))
    i += 1

if not dry_run:
    print("Not a dry run adding pairs to file")
    with open('prev_pairs.txt', 'a') as fp:
        pair_str = ""
        for name in pair:
            pair_str += "\"{}\" ".format(name)
        fp.write("{}\n".format(pair_str))
    print("Written {} pairs".format(len(res)))
