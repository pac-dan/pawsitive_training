import csv
import json
import os
import ast
import requests

# Use the relative path for your CSV file:
csv_file_path = os.path.join('data', 'chewy_scraper_sample.csv')
fixture_output_path = os.path.join('products', 'fixtures', 'products_fixture.json')
media_dir = os.path.join('media', 'products')  # Directory to store downloaded images

# Ensure that the media directory exists
os.makedirs(media_dir, exist_ok=True)

fixtures = []
pk_counter = 1

with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # first 27 products
        if pk_counter > 50:
            break
        
        # Extract and parse the images field (assumes a string representation of a list)
        images_field = row.get('images', '')
        try:
            images_list = ast.literal_eval(images_field)
            first_image_url = images_list[0] if images_list else ''
        except Exception as e:
            first_image_url = ''
        
        # Download the image locally if a URL is available
        local_image_path = ''
        if first_image_url:
            try:
                response = requests.get(first_image_url, timeout=10)
                if response.status_code == 200:
                    filename = f"{pk_counter}.jpg"
                    local_image_path = os.path.join('products', filename)  # Relative to MEDIA_ROOT
                    with open(os.path.join(media_dir, filename), 'wb') as img_file:
                        img_file.write(response.content)
                    print(f"Downloaded image for product {pk_counter}")
                else:
                    print(f"Failed to download image: {first_image_url}")
            except Exception as e:
                print(f"Error downloading image for product {pk_counter}: {e}")
        
        # Clean the price field
        raw_price = row.get('Price', '0')
        clean_price = raw_price.replace('$', '').replace(',', '').strip()
        
        # Build fixture entry
        fixture = {
            "model": "products.product",
            "pk": pk_counter,
            "fields": {
                "sku": row.get('sku', ''),
                "name": row.get('name', ''),
                "description": row.get('description', ''),
                "price": clean_price,
                "image": local_image_path,
                "brand": row.get('brand', '')
            }
        }
        fixtures.append(fixture)
        pk_counter += 1

os.makedirs(os.path.dirname(fixture_output_path), exist_ok=True)

with open(fixture_output_path, mode='w', encoding='utf-8') as jsonfile:
    json.dump(fixtures, jsonfile, indent=4)

print(f"Fixture created at: {fixture_output_path}")
print("Done!")