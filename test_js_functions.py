import json

# Test the convertProductNumbers function logic in Python
def convert_product_numbers(product):
    """Convert string values to numbers like the JavaScript function does"""
    converted = product.copy()
    if 'gst_rate' in converted and isinstance(converted['gst_rate'], str):
        converted['gst_rate'] = float(converted['gst_rate'])
    if 'selling_rate' in converted and isinstance(converted['selling_rate'], str):
        converted['selling_rate'] = float(converted['selling_rate'])
    if 'purchase_rate' in converted and isinstance(converted['purchase_rate'], str):
        converted['purchase_rate'] = float(converted['purchase_rate']) if converted['purchase_rate'] else None
    return converted

# Test with mock API data (strings)
mock_product = {
    "product_id": 1,
    "name": "Test Product",
    "sku": "TP-001",
    "pack_size": "1 kg",
    "gst_rate": "18.00",  # String from API
    "selling_rate": "100.00",  # String from API
    "purchase_rate": "80.00"
}

print("Original product data:")
print(json.dumps(mock_product, indent=2))

# Convert the product
converted_product = convert_product_numbers(mock_product)

print("\nConverted product data:")
print(json.dumps(converted_product, indent=2))

# Check types
print("\nType checks:")
print(f"- gst_rate: {type(converted_product['gst_rate'])} ({converted_product['gst_rate']})")
print(f"- selling_rate: {type(converted_product['selling_rate'])} ({converted_product['selling_rate']})")

# Test calculations
quantity = 2
line_amount = quantity * converted_product['selling_rate']
taxable_value = line_amount / (1 + (converted_product['gst_rate'] / 100))
item_gst = line_amount - taxable_value
sgst = item_gst / 2
cgst = item_gst / 2

print("\nCalculations:")
print(f"- Line Amount: {line_amount}")
print(f"- Taxable Value: {taxable_value}")
print(f"- Total GST: {item_gst}")
print(f"- SGST: {sgst}")
print(f"- CGST: {cgst}")

print("\nTest completed successfully!")