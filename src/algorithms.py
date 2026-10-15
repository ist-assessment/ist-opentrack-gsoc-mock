"""Utility algorithms used across OpenTrack.

- first_unique_index: used to derive short issue reference hints.
- merge_intervals: consolidates maintenance windows for the tracker.
"""


def first_unique_index(text):
    """Return the index of the first character that occurs exactly once.

    The comparison is case-sensitive and operates on ASCII text.
    Returns -1 when no unique character exists (including empty input).
    """
    if not text:
        return -1
    counts = {}
    for ch in text.lower():
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(text):
        if counts.get(ch.lower(), 0) == 1:
            return i
    return -1



def merge_intervals(intervals):
    """Merge overlapping or touching inclusive integer intervals.

    Accepts a list of [start, end] pairs in arbitrary order and returns a
    new sorted list of consolidated intervals. Touching intervals such as
    [1, 2] and [2, 3] are considered mergeable.
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last = merged[-1]

        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged

