#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
    format_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Describe what one usable encounter looks like.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # Read "r" the file located at `data_path` as 'data.file' with UTF-8 encoding (https://www.reddit.com/r/html5/comments/b5amwt/what_is_utf8_im_new_to_this/)
    with data_path.open("r", encoding = "utf-8") as data_file:
        # , and assign the lines to `rows`.
        rows = data_file.readlines()

    # Initialize an empty list for the usable encounters 
    encounters = []
        # and a counter for skipped rows.
    skipped_rows = 0

        # Read the rows and skip the header line.
    for row in rows[1:]:                      # rows[0] is the header line
        if not row.strip():                   # an empty line is a blank row, which can happen at the end of a CSV file
            print("Skipping a blank row.")
            skipped_rows += 1 # count every skipped row, so you can see how many were dropped
            continue
        fields = row.strip().split(",") # Python method used to remove leading and trailing whitespace
            
        if len(fields) != 3:                   # Keep a row only when it has three fields    
            # an extra comma leaves too many pieces to unpack
        # Count every other data row as skipped, the blank line included,
            # and print one line per skipped row so you can see what dropped out.
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}") 
            skipped_rows += 1 # Include these skipped rows in the count, so you can see how many were dropped
            continue
        patient_id, visit_date, systolic = fields
        try:
            systolic = int(systolic) # int() can read the systolic field, and the reading is plausible.
        except ValueError as error: # if int() cannot read the systolic field, print the patient ID and the error message, 
            print(f"Skipping {patient_id}: {error}")
            skipped_rows += 1 # and count it as a skipped row.
        else:
            if systolic < 60 or systolic > 250: # If systolic measurement is implausible, print the patient ID and the reading,
                print(f"Skipping {patient_id}: implausible systolic {systolic}")
                skipped_rows += 1 #  and count it as a skipped row.
            else:
                encounters.append({"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic})
    return encounters, skipped_rows         # End with `return encounters, skipped`.
    # pass (placeholder for the function body, so you can run the script before you write the function)


def main():
    """Describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    """Build, save, and verify a small vitals report."""
    # Read filepath 
    data_path = DATA_PATH
    # If filepath non-existent, 
    if not data_path.exists():
        # Print it's non-existent
        print(f"Cannot find {data_path}: run this script from clinic_report.")
        return

    # Run  `read_encounters` function created above on the file path
    encounters, skipped_rows = read_encounters(data_path)
    # If every row were unusable there would be nothing to average, 
        # so assert encounters, state that expectation before the script formats anything. 
    assert encounters, f"no usable readings in {data_path}"
    
    # Assign systolic readings into the `readings` object
    readings = systolic_readings(encounters)
    
    # Extract patient_id and systolic reading in `encounters`
    lines = format_readings(encounters)

    # Build the six report lines and write them to output/vitals_report.txt.
        # a) Print how many data rows were usable
    lines.append(f"Usable encounters: {len(encounters):.1f} rows")
        # b) Print how many data rows were skipped
    lines.append(f"Skipped rows: {skipped_rows} rows")
        # c) Print how many different patient IDs appear among the usable encounters
    lines.append(f"Patients seen: {count_patients(encounters):.1f} rows")
        # d) Print the mean systolic pressure
    lines.append(f"Mean systolic: {mean_systolic(readings):.1f} mmHg")
        # e) Print the highest systolic pressure
    lines.append(f"Highest systolic: {max(readings)} mmHg")
        # f) Print the lowest systolic pressure
    lines.append(f"Lowest systolic: {min(readings)} mmHg")
    report_text = "\n".join(lines) + "\n"

    """ Write the report to a file in the output directory, 
    creating the directory if it doesn't exist """
    report_path = OUTPUT_DIR / "vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

    """Choose your follow-up cutoff, then write output/followup_list.txt
    with the Cutoff line, the Reason line, and one patient ID per line."""

    # Set up a cutoff value for systolic readings, and find all patient IDs with readings at or above that cutoff. 
        # When you run the script, it will prompt you to enter a cutoff value at the terminal. 
    cutoff = int(input("Cutoff (mmHg): "))

    # Flag all patient IDs with systolic readings at or above the cutoff, and add this to the 'flagged' list. 
    flagged = []

    # Iterate through the encounters, and if the systolic reading is at or above the cutoff, add the patient ID to the 'flagged' list.
    print(encounters)
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            flagged.append(encounter["patient_id"])
    print("Flagged:", flagged)

    # Create a list of strings to write to the follow-up file, starting with the cutoff and reason lines, followed by the flagged patient IDs.
    flagged_list = [f"Cutoff: {cutoff} mmHg", f"Reason: Systolic >={cutoff} mmHg considered hypertensive"] + flagged 
    # Join the list into a single string with newline characters between each line, and add a final newline at the end.
    flagged_text = "\n".join(flagged_list) + "\n"

    # Write the flagged patient IDs to the follow-up file in the output directory, creating the directory if it doesn't exist.
    followup_path = OUTPUT_DIR / "followup_list.txt"
    # Write "w" to the file, which will create the file if it doesn't exist, or overwrite it if it does. 
        # Use UTF-8 encoding to ensure that any non-ASCII characters are handled correctly.
    with open(followup_path, "w", encoding="utf-8") as followup_file:
        followup_file.write(flagged_text)

    # Do not run any function in any other script below this line.
if __name__ == "__main__":
    main()
