"""Lab 4 — Word Count, the lecture's two sentences, with a combiner."""

from collections import Counter
from mini_mr import mapreduce

DOCS = [
    (0, "the cat sat on the mat"),
    (1, "the dog sat on the log"),
]


def tokenize(line):
    return line.lower().split()


def mapper(offset, line):
    for word in tokenize(line):
        yield word, 1


def combiner(word, ones):
    # Sum is commutative and associative, so a local combine is safe.
    yield word, [sum(ones)]


def reducer(word, values):
    yield word, sum(values)


counts = dict(mapreduce(DOCS, mapper, reducer, combiner))
# The deck prints (the, 3). Both sentences contain two "the"s, so the total is 4.
expected = {"the": 4, "cat": 1, "sat": 2, "on": 2, "mat": 1, "dog": 1, "log": 1}
print("Word count:")
for word in sorted(counts):
    print(f"  {word}: {counts[word]}")
assert counts == expected
print("Deck total for 'the' is 3. Tokenising both full sentences gives 4.")

# Unsafe combiner: average is not safe if you average the averages.
partial = [10, 30]
bad = sum(partial) / len(partial)  # 20, which happens to match
# Two groups of different sizes: avg(avg(1,1,1), avg(100)) != avg(1,1,1,100)
wrong = ((1 + 1 + 1) / 3 + 100 / 1) / 2
right = (1 + 1 + 1 + 100) / 4
print(f"Unsafe combiner example (average): combined={wrong:.1f} true={right:.1f}")
assert wrong != right
print("Combiner is safe for sum, not for a plain average.")
