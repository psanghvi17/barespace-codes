import json
import csv

def json_to_csv(json_file, csv_file):
    # Open and load the JSON file with utf-8 encoding
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except UnicodeDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return

    # Prepare the data to be written into CSV
    csv_data = []

    # Check if the input JSON is an array or single object
    if isinstance(data, list):
        objects = data
    else:
        objects = [data]

    for obj in objects:
        attributes = obj.get("attributes", {})
        relationships = obj.get("relationships", {})

        # Extract category type
        category = relationships.get("category", {}).get("data", {}).get("id")
        
        # Extract employee names
        employees = relationships.get("employees", {}).get("data", [])
        employee_names = ", ".join([employee.get("id") for employee in employees])

        row = {
            "name": attributes.get("name"),
            "book-online": attributes.get("book-online"),
            "non-discounted-price": attributes.get("non-discounted-price"),
            "retail-price": attributes.get("retail-price"),
            "description": attributes.get("description"),
            "duration-value": attributes.get("duration-value"),
            "category": category,
            "employee-names": employee_names,
        }
        csv_data.append(row)

    # Define the CSV headers
    headers = ["name", "book-online", "non-discounted-price", "retail-price", "description", "duration-value", "category", "employee-names"]

    # Write the data to the CSV file with utf-8 encoding
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"Data successfully written to {csv_file}")
    except UnicodeEncodeError as e:
        print(f"Error writing to CSV file: {e}")

# Example usage
json_file = 'fresha-services.json'  # Replace with your JSON file
csv_file = 'output.csv'  # Replace with your desired CSV file name
json_to_csv(json_file, csv_file)