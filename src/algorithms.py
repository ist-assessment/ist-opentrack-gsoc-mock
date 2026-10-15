
"""Utility algorithms used across OpenTrack."""


def first_unique_index(text):
    """Return the index of the first character occurring exactly once."""
    counts = {}

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    for index, char in enumerate(text):
        if counts[char] == 1:
            return index

    return -1


def merge_intervals(intervals):
    """Merge overlapping or touching inclusive integer intervals."""
    if not intervals:
        return []

    sorted_intervals = sorted([list(interval) for interval in intervals])
    merged = [sorted_intervals[0]]

    for start, end in sorted_intervals[1:]:
        last = merged[-1]

        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged
