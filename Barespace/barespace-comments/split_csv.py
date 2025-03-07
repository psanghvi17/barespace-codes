import csv
import os

def split_csv(input_file, output_dir, rows_per_file=500):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header row

        file_count = 0
        rows = []

        for row_count, row in enumerate(reader, start=1):
            rows.append(row)
            # When rows_per_file rows are collected, write to a new file
            if row_count % rows_per_file == 0:
                file_count += 1
                output_file = os.path.join(output_dir, f'output_part_{file_count}.csv')
                with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)  # Write the header row
                    writer.writerows(rows)  # Write the collected rows
                rows = []  # Reset the rows buffer

        # Write any remaining rows to a final file
        if rows:
            file_count += 1
            output_file = os.path.join(output_dir, f'output_part_{file_count}.csv')
            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(rows)

    print(f"Split completed: {file_count} files created in '{output_dir}'.")

# Example usage
input_csv = 'PhoneNumbers.csv'  # Path to your input CSV file
output_directory = 'split_files'  # Directory where split files will be saved
split_csv(input_csv, output_directory)
