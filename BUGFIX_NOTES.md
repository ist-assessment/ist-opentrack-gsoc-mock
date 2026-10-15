# Bug Fix Notes

## Defects Fixed

1. Fixed priority ordering to high, medium, then low.
2. Fixed issue ID ordering to ascending order within each priority.
3. Fixed filtering to include only issues with status exactly "open".
4. Fixed limit handling so zero returns an empty list.
5. Prevented modification of the original input collection.

## Tests Added

- Open-status filtering
- Priority ordering
- Ascending ID ordering
- Zero-limit handling
- Result-limit handling
- Input immutability

## Test Command

Run the tests using:

python -m pytest -q