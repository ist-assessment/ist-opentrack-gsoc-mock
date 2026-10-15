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
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        last = merged[-1]
        if start < last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged



"""
Utility algorithms used across OpenTrack.

Functions:
    first_unique_index: Find the first unique character.
    merge_intervals: Merge overlapping integer intervals.
"""

from collections import Counter
from typing import Sequence


def first_unique_index(
    text: str,
    *,
    case_sensitive: bool = False
) -> int:
    """
    Return the index of the first character occurring exactly once.

    Args:
        text: Input string.
        case_sensitive: If True, compare characters by exact case.

    Returns:
        Index of the first unique character, or -1 if none exists.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if case_sensitive:
        normalized = text
    else:
        normalized = text.lower()

    counts = Counter(normalized)

    for index, char in enumerate(normalized):
        if counts[char] == 1:
            return index

    return -1


def merge_intervals(
    intervals: Sequence[Sequence[int]],
    *,
    merge_touching: bool = True
) -> list[list[int]]:
    """
    Merge overlapping or optionally touching inclusive intervals.

    Args:
        intervals: Sequence of [start, end] pairs.
        merge_touching: Merge intervals sharing an endpoint.

    Returns:
        A new sorted list of merged intervals.

    Raises:
        TypeError: If the input or interval values have invalid types.
        ValueError: If an interval is malformed or reversed.
    """
    if not isinstance(merge_touching, bool):
        raise TypeError("merge_touching must be a boolean")

    if not isinstance(intervals, (list, tuple)):
        raise TypeError("intervals must be a list or tuple")

    normalized = []

    for interval in intervals:
        if not isinstance(interval, (list, tuple)):
            raise TypeError("each interval must be a list or tuple")

        if len(interval) != 2:
            raise ValueError("each interval must contain two values")

        start, end = interval

        # bool is a subclass of int, so reject it explicitly.
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, int)
            or not isinstance(end, int)
        ):
            raise TypeError("interval endpoints must be integers")

        if start > end:
            raise ValueError("interval start cannot exceed its end")

        normalized.append([start, end])

    if not normalized:
        return []

    normalized.sort(key=lambda interval: interval[0])
    merged = [normalized[0]]

    for start, end in normalized[1:]:
        last = merged[-1]

        overlaps = start <= last[1] if merge_touching else start < last[1]

        if overlaps:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged


__all__ = ["first_unique_index", "merge_intervals"]


