import pandas as pd
from datetime import datetime

# Load the input CSV file with appropriate encoding
file_path = 'unique_client_appointments.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Define a function to convert date format in the 'Scheduled on' column
def convert_date_to_yymmdd_with_time(date_string):
    try:
        # Split the date and time
        split_date_time = date_string.rsplit(' ', 2)  # Splitting at the last two parts for time
        date_part = ' '.join(split_date_time[:-2])  # Extract 'Tuesday 26 November 2024'
        time_part = ' '.join(split_date_time[-2:])  # Extract '2:45 pm'

        # Parse the date part
        original_date = datetime.strptime(date_part, '%A %d %B %Y')  # Parse original date format
        formatted_date = original_date.strftime('%y%m%d')  # Convert date to YYMMDD

        # Combine formatted date and original time
        return f"{formatted_date} {time_part}"
    except Exception as e:
        print(f"Error parsing date and time: {date_string}, error: {e}")
        return date_string  # Return original value if parsing fails

# Apply the function to the 'Scheduled on' column
data['Scheduled on'] = data['Scheduled on'].apply(convert_date_to_yymmdd_with_time)

# Save the updated DataFrame to a new file
output_file_path = 'client_appointments_yymmdd_with_time.csv'
data.to_csv(output_file_path, index=False)

print(f"File with updated date and time format created at: {output_file_path}")
