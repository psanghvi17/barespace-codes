import csv

csv_file = "client_notes.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Notes"])
    # Write the notes value
    writer.writerow(["notes_value"])