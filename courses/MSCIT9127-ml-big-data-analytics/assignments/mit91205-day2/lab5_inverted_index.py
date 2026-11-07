"""Lab 5 — inverted index: term -> document ids."""

from mini_mr import mapreduce

DOCS = [
    ("doc1", "the cat sat on the mat"),
    ("doc2", "the dog sat on the log"),
]


def mapper(doc_id, content):
    for word in content.lower().split():
        yield word, doc_id


def reducer(term, doc_ids):
    postings = sorted(set(doc_ids))
    yield term, postings


index = dict(mapreduce(DOCS, mapper, reducer))
print("Inverted index:")
for term in sorted(index):
    print(f"  {term}: {index[term]}")

assert index["the"] == ["doc1", "doc2"]
assert index["cat"] == ["doc1"]
assert index["dog"] == ["doc2"]
assert index["sat"] == ["doc1", "doc2"]
print("Shuffle grouped every document for a term onto one reducer.")
