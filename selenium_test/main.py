from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(by, value, timeout=10):
    """
    Waits for an element to be present in the DOM.
    Returns the WebElement once found or raises TimeoutException after timeout.
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def go_to_cart():
    cart_button = driver.find_element(By.CSS_SELECTOR, "#_desktop_cart a")
    cart_button.click()

def id_element_write(element_id: str, text: str):
    driver.find_element(By.ID, element_id).send_keys(text)

def wait(time_s: int = 1):
    time.sleep(time_s)

def add_to_cart(quantity: int = 1):
    product_plus_quantity = driver.find_element(By.CSS_SELECTOR,"button.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up")
    product_minus_quantity = driver.find_element(By.CSS_SELECTOR,"button.btn.btn-touchspin.js-touchspin.bootstrap-touchspin-down")

    for _ in range(quantity-1):
        product_plus_quantity.click()

    wait()

    while driver.find_elements(By.CSS_SELECTOR, "i.material-icons.product-unavailable"):
        product_minus_quantity.click()
        wait()

    add_to_cart_btn = driver.find_element(By.XPATH, "//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[2]/button")
    add_to_cart_btn.click()

    wait()

    continue_button = driver.find_element(By.XPATH,"//*[@id=\"blockcart-modal\"]/div/div/div[2]/div/div[2]/div/div/button")
    continue_button.click()

    wait()

    while(True):
        driver.back()
        try:
            driver.find_element(By.ID, "js-product-list")
            break
        except NoSuchElementException:
            continue

    wait()


# 10 products, different quantity, from two categories
def add_products_to_cart():

    categories_no = 2
    products_no = 10

    wait()

    category_id = 85
    while categories_no > 0 or products_no > 0:
        products_init_no = products_no

        # <-- Use wait_for_element here instead of find_element directly
        products_panel = wait_for_element(By.ID, "category-3")
        ActionChains(driver).move_to_element(products_panel).perform()

        wait()

        category_found = False

        while not category_found:
            category_elements = driver.find_elements(By.ID, "category-" + str(category_id))
            if category_elements:
                category_elements[0].click()
                category_found = True
            category_id += 1

        wait()

        products = driver.find_elements(By.CSS_SELECTOR, "div.js-product.product")

        for i in range(len(products)):

            products = driver.find_elements(By.CSS_SELECTOR, "div.js-product.product")

            if products[i].find_elements(By.CSS_SELECTOR, "li.product-flag.out_of_stock"):
                continue

            # Wait for the clickable thumbnail before clicking
            thumbnail = wait_for_element(By.CSS_SELECTOR, ".js-product a.product-thumbnail")
            products[i].find_element(By.CSS_SELECTOR, ".js-product a.product-thumbnail").click()

            wait()

            add_to_cart(random.randint(1,5))
            products_no -= 1

            if not ((categories_no >= 2 and products_no > 3) or (categories_no == 1 and products_no > 0)):
                break

        if products_init_no > products_no:
            categories_no -= 1

        wait()



# add random product to cart
def search_for_product():
    search_box = driver.find_element(By.NAME, "s")
    search_box.send_keys("piękna klameczka")

    wait()

    search_box.send_keys(Keys.ENTER)

    wait()

    products = driver.find_elements(By.CSS_SELECTOR, "div.js-product.product")

    found = False
    while not found:
        random_product = random.choice(products)
        if random_product.find_elements(By.CSS_SELECTOR, "li.product-flag.out_of_stock"):
            continue
        else:
            random_product.find_element(By.CSS_SELECTOR, ".js-product a.product-thumbnail").click()
            found = True

    add_to_cart()


# remove 3 products from cart
def remove_products():
    go_to_cart()

    wait()

    for _ in range(3):
        remove_product_btns = driver.find_elements(By.CSS_SELECTOR, "a.remove-from-cart")
        random.choice(remove_product_btns).click()
        wait()

    driver.back()

    wait()


# create new account
def register():
    login_btn = driver.find_element(By.CSS_SELECTOR, "div.user-info")
    login_btn.click()

    wait()

    register_btn = driver.find_element(By.CSS_SELECTOR, "div.no-account")
    register_btn.click()

    wait()

    driver.find_element(By.ID, "field-id_gender-1").click()

    wait()

    id_element_write("field-firstname", "Konrad")

    wait()

    id_element_write("field-lastname", "Pawłowski")

    wait()

    id_element_write("field-email", "konrad.pawlowski23@gmail.com")

    wait()

    id_element_write("field-password", "tajemnica67")

    wait()

    finish_btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit.float-xs-right")
    driver.execute_script("arguments[0].scrollIntoView();", finish_btn)

    wait()

    driver.find_element(By.NAME, "customer_privacy").click()

    wait()

    driver.find_element(By.NAME, "psgdpr").click()

    wait()

    email_no = 23
    while(True):
        email_no += 1
        finish_btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.form-control-submit.float-xs-right")
        driver.execute_script("arguments[0].scrollIntoView();", finish_btn)
        finish_btn.click()
        wait()
        try:
            driver.find_element(By.CSS_SELECTOR, "li.alert.alert-danger")
            driver.find_element(By.ID, "field-email").clear()
            id_element_write("field-email", "konrad.pawlowski" + str(email_no) + "@gmail.com")
            id_element_write("field-password", "tajemnica67")
            wait()
        except NoSuchElementException:
            break

    wait()




# order products from cart
def order_products():
    # payment on site
    # choose one of the carriers
    # accept

    go_to_cart()

    wait()

    driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary").click()

    wait()

    id_element_write("field-address1", "Nie podam :D")

    wait()

    id_element_write("field-postcode", "12-345")

    wait()

    id_element_write("field-city", "Gdańsk")

    wait()

    continue_btn = driver.find_element(By.NAME, "confirm-addresses")
    driver.execute_script("arguments[0].click();", continue_btn)

    wait()

    input_radio = driver.find_element(By.ID, "delivery_option_6")
    driver.execute_script("arguments[0].click();", input_radio)

    wait()

    continue_btn = driver.find_element(By.NAME, "confirmDeliveryOption")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", continue_btn)
    driver.execute_script("arguments[0].click();", continue_btn)

    wait()

    payment_label = driver.find_element(By.CSS_SELECTOR, "label[for='payment-option-3']")
    payment_label.click()

    wait()

    terms_checkbox = driver.find_element(By.CSS_SELECTOR, "input[id^='conditions_to_approve']")
    driver.execute_script("arguments[0].click();", terms_checkbox)

    wait()

    driver.execute_script("document.getElementById('payment-form').submit();")

    wait()


#checking order status
def order_status():

    driver.find_element(By.CSS_SELECTOR, "a.account").click()

    wait()

    driver.find_element(By.ID, "history-link").click()

    wait()

    driver.find_element(By.CSS_SELECTOR, 'a[data-link-action="view-order-details"]').click()

    wait(2)

    driver.back()

    wait()


# download VAT invoice
def vat_invoice():
    link = driver.find_element(By.XPATH, "//a[contains(@href,'controller=pdf-invoice')]")
    link.click()

    wait()


driver = webdriver.Chrome()

print("Test started")

driver.get("https://localhost:8080")
driver.maximize_window()

add_products_to_cart()
search_for_product()
remove_products()
register()
order_products()
order_status()
vat_invoice()

driver.quit()

print("Test finished")