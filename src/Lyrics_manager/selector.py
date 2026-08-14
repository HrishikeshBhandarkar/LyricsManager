# Script to select audio files from the scanned dictionary whose lyrics the user wishes to find.

def selector(indices: list[int], data: dict[int, dict]) -> dict[int, dict]:
    """
    Filters the scanned dictionary based on user-selected 1-based indices.
    - If 0 is in indices, returns the full scanned dictionary.
    - Returns a filtered dictionary of selected tracks, or None if any index is invalid.
    """
    result = {}

    # If 0 is in selection, user selected all scanned files
    if 0 in indices:
        return data

    # WHY WE CHANGED THIS TO A DICTIONARY LOOKUP:
    # Now that 'data' is a dictionary keyed by 1-based index integers (1, 2, 3...),
    # we directly check 'if i in data:' without needing 'i - 1' list index arithmetic.
    for i in indices:
        if i in data:
            result[i] = data[i]
        else:
            # Return None if an out-of-bounds index was selected
            return {} 

    return result  # Returns dictionary of selected track metadata objects
