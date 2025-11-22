from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

def go_to_cart():
    cart_button = driver.find_element(By.CSS_SELECTOR, "#_desktop_cart a")
    cart_button.click()

def id_element_write(element_id: str, text: str):
    driver.find_element(By.ID, element_id).send_keys(text)

def wait(time_s: int = 1):
    time.sleep(time_s)

def add_to_cart(quantity: int = 1):
    product_plus_quantity = driver.find_element(By.XPATH,"//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[1]/div/span[3]/button[1]")

    for _ in range(quantity-1):
        product_plus_quantity.click()

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
    wait()

    products_panel = driver.find_element(By.ID, "category-3")
    ActionChains(driver).move_to_element(products_panel).perform()

    wait()

    #first category

    category_a = driver.find_element(By.ID, "category-4")
    category_a.click()

    wait()

    #first product

    products = driver.find_elements(By.CSS_SELECTOR, ".js-product a.product-thumbnail")
    products[0].click()

    wait()

    add_to_cart(2)

# add random product to cart
def search_for_product():
    search_box = driver.find_element(By.NAME, "s")
    search_box.send_keys("T-Shirt")

    wait()

    search_box.send_keys(Keys.ENTER)

    wait()

    products = driver.find_elements(By.CSS_SELECTOR, ".js-product a.product-thumbnail")
    random_product = random.choice(products)
    random_product.click()

    add_to_cart()


# remove 3 products from cart
def remove_products():
    go_to_cart()

    wait()

    remove_product_btn = driver.find_element(By.CSS_SELECTOR, "a.remove-from-cart")
    remove_product_btn.click()

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

    input_radio = driver.find_element(By.ID, "delivery_option_2")
    driver.execute_script("arguments[0].click();", input_radio)

    wait()

    continue_btn = driver.find_element(By.NAME, "confirmDeliveryOption")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", continue_btn)
    driver.execute_script("arguments[0].click();", continue_btn)

    wait()

    payment_label = driver.find_element(By.CSS_SELECTOR, "label[for='payment-option-1']")
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

    wait()

# download VAT invoice
def vat_invoice():
    pass

driver = webdriver.Chrome()

print("Test started")

driver.get("http://localhost:8080/")
driver.maximize_window()

add_products_to_cart()
search_for_product()
remove_products()
register()
add_products_to_cart() # <--- TODO delete
order_products()
order_status()
vat_invoice()

driver.quit()

print("Test finished")