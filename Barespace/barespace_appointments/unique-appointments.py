import pandas as pd
# Select relevant columns for uniqueness
columns_for_uniqueness = ['Client Name', 'Client Lastname', 'Service', 'Price', 'Scheduled on']

file_path = 'client_appointments_25-11.csv'  # Replace this with the actual file path
data = pd.read_csv(file_path,encoding='latin1')

# Drop duplicate rows based on the selected columns
unique_data = data.drop_duplicates(subset=columns_for_uniqueness)

# Save the unique rows to a new file
output_file_path = 'unique_client_appointments.csv'
unique_data.to_csv(output_file_path, index=False)

output_file_path
