from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Visit a page
@when('I visit the "{page}"')
def step_impl(context, page):
    urls = {
        "Home Page": context.base_url
    }
    context.driver.get(urls[page])

# Set a field value
@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    element_id = field.lower()
    elem = context.driver.find_element(By.ID, element_id)
    elem.clear()
    elem.send_keys(value)

# Press a button
@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()

# Copy field value to context
@when('I copy the "{field}" field')
def step_impl(context, field):
    element_id = field.lower()
    context.copied_value = context.driver.find_element(By.ID, element_id).get_attribute('value')

# Paste copied value into a field
@when('I paste the "{field}" field')
def step_impl(context, field):
    element_id = field.lower()
    elem = context.driver.find_element(By.ID, element_id)
    elem.clear()
    elem.send_keys(context.copied_value)

# Clear a field
@when('I press the "Clear" button')
def step_impl(context):
    context.driver.find_element(By.ID, 'clear-btn').click()

# Verify a specific message is present
@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert(found)

# Verify a specific name/text is in the results
@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert(found)

# Verify a specific name/text is NOT in the results
@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert(name not in element.text)

# Verify field values
@then('I should see "{value}" in the "{field}" field')
def step_impl(context, value, field):
    element_id = field.lower()
    elem_value = context.driver.find_element(By.ID, element_id).get_attribute('value')
    assert(elem_value == value)

# Verify dropdown values
@then('I should see "{value}" in the "{field}" dropdown')
def step_impl(context, value, field):
    element_id = field.lower()
    elem = context.driver.find_element(By.ID, element_id)
    selected_value = elem.get_attribute('value')
    assert(selected_value == value)
