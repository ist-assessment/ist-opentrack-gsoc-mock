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

    # Count frequency of each character keeping case sensitivity intact
    char_counts = {}
    for character in text:
        if character in char_counts:
            char_counts[character] = char_counts[character] + 1
        else:
            char_counts[character] = 1

    # Find the index of the first character with a count of exactly 1
    for index in range(len(text)):
        current_char = text[index]
        if char_counts[current_char] == 1:
            return index

    return -1


def merge_intervals(intervals):
    """Merge overlapping or touching inclusive integer intervals.

    Accepts a list of [start, end] pairs in arbitrary order and returns a
    new sorted list of consolidated intervals. Touching intervals such as
    [1, 2] and [2, 3] are considered mergeable.
    """
    if not intervals:
        return []

    # First sort the intervals based on the starting times
    sorted_intervals = sorted(intervals)

    # Start our merged list with the first sorted interval item
    final_merged = []
    final_merged.append(list(sorted_intervals[0]))

    # Loop through the rest of the intervals step-by-step
    for i in range(1, len(sorted_intervals)):
        current_interval = sorted_intervals[i]
        current_start = current_interval[0]
        current_end = current_interval[1]

        last_merged_interval = final_merged[-1]

        # Check if the intervals overlap or touch each other (inclusive matching)
        if current_start <= last_merged_interval[1]:
            # Update the end boundary to include the maximum point
            if current_end > last_merged_interval[1]:
                last_merged_interval[1] = current_end
        else:
            # No overlap or touch, add it as a standalone clean window
            final_merged.append([current_start, current_end])

    return final_merged
