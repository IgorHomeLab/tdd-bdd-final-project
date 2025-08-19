import requests
from http import HTTPStatus

# Assuming rest_endpoint is already defined, e.g.
# rest_endpoint = "http://localhost:5000/products"

# Step to delete all products (already provided)
def delete_all_products():
    response = requests.get(rest_endpoint)
    products = response.json()
    for product in products:
        requests.delete(f"{rest_endpoint}/{product['id']}")

# Step to load background data
def before_scenario(context, scenario):
    # Delete all existing products first
    delete_all_products()

    # Load products from background table
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],  # convert string to boolean
            "category": row['category']
        }

        # Send POST request to REST API
        context.resp = requests.post(rest_endpoint, json=payload)

        # Ensure product was created successfully
        assert context.resp.status_code == HTTPStatus.CREATED
