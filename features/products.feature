Feature: Product Admin UI

  Background:
    Given the following products exist
      | name  | description      | price | available | category |
      | Hat   | A red fedora     | 59.95 | True      | Cloths   |
      | Shoes | Running shoes    | 89.99 | True      | Footwear |
      | Bag   | Leather backpack | 120.0 | False     | Bags     |

  Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Cloths" in the "Category" dropdown
    And I should see "59.95" in the "Price" field

  Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I set the "Price" to "64.95"
    And I press the "Update" button
    Then I should see the message "Success"
    And I should see "64.95" in the "Price" field

  Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Shoes"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Delete" button
    Then I should see the message "Success"
    And I should not see "Shoes" in the product list

  Scenario: List all Products
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see the message "Success"
    And I should see "Hat" in the product list
    And I should see "Shoes" in the product list
    And I should see "Bag" in the product list

  Scenario: Search for Products by Category
    When I visit the "Home Page"
    And I set the "Category" to "Bags"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Bag" in the product list
    And I should not see "Hat" in the product list
    And I should not see "Shoes" in the product list

  Scenario: Search for Products by Availability
    When I visit the "Home Page"
    And I set the "Available" dropdown to "True"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the product list
    And I should see "Shoes" in the product list
    And I should not see "Bag" in the product list

  Scenario: Search for Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Bag"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Bag" in the product list
    And I should not see "Hat" in the product list
    And I should not see "Shoes" in the product list
