from service.common import status
from service.models import Category
from .factories import ProductFactory

BASE_URL = "/products"

class TestProductRoutes(...):
    # NOTE: assuming your class already has setUp/tearDown and helper:
    # self._create_products(n) -> returns list of created Product dicts

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product["name"])

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products(1)[0]
        product_id = test_product["id"]

        # make a new body using a factory
        updated = ProductFactory().serialize()
        updated["id"] = product_id  # id must match path id
        updated["description"] = "updated description"

        resp = self.client.put(
            f"{BASE_URL}/{product_id}",
            json=updated,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], product_id)
        self.assertEqual(data["description"], "updated description")

        # read it back to verify
        resp = self.client.get(f"{BASE_URL}/{product_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["description"], "updated description")

    def test_update_product_not_found(self):
        """It should return 404 when updating non-existent Product"""
        updated = ProductFactory().serialize()
        updated["id"] = 0
        resp = self.client.put(f"{BASE_URL}/0", json=updated, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        product_id = test_product["id"]

        resp = self.client.delete(f"{BASE_URL}/{product_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it is gone
        resp = self.client.get(f"{BASE_URL}/{product_id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_products(self):
        """It should List all Products"""
        products = self._create_products(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(products))

    def test_query_products_by_name(self):
        """It should List Products filtered by name"""
        products = self._create_products(5)
        # force a known name on two products
        target_name = "Apple"
        for i in range(2):
            pid = products[i]["id"]
            body = products[i]
            body["name"] = target_name
            self.client.put(f"{BASE_URL}/{pid}", json=body, content_type="application/json")

        resp = self.client.get(f"{BASE_URL}?name={target_name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertTrue(len(data) >= 2)
        for item in data:
            self.assertEqual(item["name"], target_name)

    def test_query_products_by_category(self):
        """It should List Products filtered by category"""
        products = self._create_products(5)
        # set 3 to a specific category
        target_category = "FOOD"
        for i in range(3):
            pid = products[i]["id"]
            body = products[i]
            body["category"] = target_category
            self.client.put(f"{BASE_URL}/{pid}", json=body, content_type="application/json")

        resp = self.client.get(f"{BASE_URL}?category={target_category}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertTrue(len(data) >= 3)
        for item in data:
            self.assertEqual(item["category"], target_category)

    def test_query_products_by_availability(self):
        """It should List Products filtered by availability"""
        products = self._create_products(6)
        # set 4 available=True, 2 available=False
        for i, prod in enumerate(products):
            pid = prod["id"]
            body = prod
            body["available"] = i < 4
            self.client.put(f"{BASE_URL}/{pid}", json=body, content_type="application/json")

        resp = self.client.get(f"{BASE_URL}?available=true")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertTrue(len(data) >= 4)
        for item in data:
            self.assertTrue(item["available"])
