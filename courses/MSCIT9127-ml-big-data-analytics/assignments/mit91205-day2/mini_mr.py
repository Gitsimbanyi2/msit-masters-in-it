"""MapReduce stand-in: split, map, optional combiner, shuffle, reduce."""

from collections import defaultdict


def mapreduce(records, mapper, reducer, combiner=None):
    """records: list of (k1, v1). Returns list of (k3, v3) sorted by key."""
    intermediate = defaultdict(list)
    for key, value in records:
        for k2, v2 in mapper(key, value):
            intermediate[k2].append(v2)

    if combiner is not None:
        combined = {}
        for k2, values in intermediate.items():
            combined[k2] = []
            for ck, cv in combiner(k2, values):
                combined[ck].extend(cv if isinstance(cv, list) else [cv])
        intermediate = combined

    output = []
    for k2 in sorted(intermediate, key=lambda k: str(k)):
        output.extend(reducer(k2, intermediate[k2]))
    return output
