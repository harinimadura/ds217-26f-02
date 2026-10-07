"""Reusable helpers for summarizing clinic systolic readings."""

def format_readings(encounters):
    """Return one display line for each encounter record."""
    lines = []
    for encounter in encounters:
        lines.append(f"{encounter['patient_id']}: {encounter['systolic']} mmHg")
    return lines
    
def systolic_readings(encounters):
    """Describe what this pulls out of the encounter records."""
    readings = []
    for encounter in encounters:
        # print(encounter)
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Describe what this returns, including the empty-list result."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Describe what this counts."""
    # Read CSV file, create a set (which only sets apart unique values)
    patients = set()
    for encounter in encounters:
        patients.add(encounter['patient_id'])
    return len(patients)


def patients_at_or_above(encounters, cutoff):
    """Describe which patient IDs come back."""
    flagged_ids = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            flagged_ids.append(encounter["patient_id"])

    flagged = set(flagged_ids)                   # the same IDs as a set, so & can compare groups
    print(f"Flagged ({cutoff} mmHg and above): {flagged_ids}")

# def highest_reading(readings):
#     """Return the largest reading, or None when there are no readings."""
#     if not readings:
#         return None
#     return max(readings)

# def lowest_reading(readings):
#     """Return the smallest reading, or None when there are no readings."""
#     if not readings:
#         return None
#     return min(readings)
  
