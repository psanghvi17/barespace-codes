import json
import csv

# Function to read JSON files
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to map category id to category name
def map_categories(categories):
    category_map = {}
    for category in categories:
        cat_id = category['id']
        cat_name = category['attributes']['name']
        category_map[cat_id] = cat_name
    return category_map

# Function to map supplier id to supplier name
def map_suppliers(suppliers):
    supplier_map = {}
    for supplier in suppliers:
        supplier_id = supplier['id']
        supplier_name = supplier['attributes']['name']
        supplier_map[supplier_id] = supplier_name
    return supplier_map

# Function to merge data and write to CSV
def create_csv(products, category_map, supplier_map, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['name', 'full-price', 'cost-price', 'barcode', 'description', 'category', 'supplier'])

        # Write product rows
        for product in products:
            attributes = product['attributes']
            relationships = product.get('relationships', {})

            product_name = attributes.get('name', '')
            full_price = attributes.get('full-price', '')
            cost_price = attributes.get('cost-price', '')
            barcode = attributes.get('barcode', '')
            description = attributes.get('description', '')

            # Safely get category id and map to name
            category = relationships.get('category')
            category_data = category.get('data') if category else None
            category_id = category_data.get('id') if category_data else None
            category_name = category_map.get(category_id, 'Unknown') if category_id else 'Unknown'

            # Safely get supplier id and map to name
            supplier = relationships.get('supplier')
            supplier_data = supplier.get('data') if supplier else None
            supplier_id = supplier_data.get('id') if supplier_data else None
            supplier_name = supplier_map.get(supplier_id, 'Unknown') if supplier_id else 'Unknown'

            # Write row
            writer.writerow([product_name, full_price, cost_price, barcode, description, category_name, supplier_name])

# Main logic
if __name__ == "__main__":
    # File paths
    categories_file = 'categories.json'
    products_file = 'fresha_products.json'
    suppliers_file = 'suppliers.json'
    output_csv = 'output.csv'

    # Read JSON files
    categories_data = read_json(categories_file)
    products_data = read_json(products_file)
    suppliers_data = read_json(suppliers_file)

    # Map categories and suppliers
    category_mapping = map_categories(categories_data)
    supplier_mapping = map_suppliers(suppliers_data)

    # Generate CSV
    create_csv(products_data, category_mapping, supplier_mapping, output_csv)

    print(f"CSV file '{output_csv}' has been created successfully.")
