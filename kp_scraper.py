from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import csv
from datetime import  datetime
today = datetime.now().strftime("%d/%m/%Y")

CSS_EXCHANGE_RATE = ".CurrencyConverter_rate___bZk1"
CSS_PAGES = ".Pagination_numbers__9OjwH"
CSS_PRODUCT = ".AdItem_adHolder__CWcMj"
CSS_NAME = ".AdItem_name__Knlo6"
CSS_PRICE = ".AdItem_price__SkT1P"
CSS_EXCHANGE_PRODUCT = ".AdItem_exchange__ZQj3Q"
CSS_LOCATION = ".AdItem_originAndPromoLocation__PmiaP > p"
CSS_INFO = ".AdItem_adInfoHolder__FYK1b p"
CSS_URL = ".Link_link__2iGTE.Link_inherit__fCY5K"

options = webdriver.ChromeOptions()
# Block images
options.add_argument("--blink-settings=imagesEnabled=false")
# Headless mode
options.add_argument("--headless=new")

input_URL = input("ENTER KUPUJEMPRODAJEM URL:\n")

driver = webdriver.Chrome(
    options=options
    )

if input_URL.endswith("&page=1"):
    URL = input_URL.removesuffix("&page=1")
else:
    URL = input_URL

print("Started scraping at " + datetime.now().strftime("%H:%M:%S"))
driver.get(URL)

exchange_rate = float(driver.find_elements(By.CSS_SELECTOR,CSS_EXCHANGE_RATE)[1].text)

try:
    page_list = driver.find_element(By.CSS_SELECTOR,CSS_PAGES).find_elements(By.TAG_NAME, "div")
    num_of_pages = page_list[-1].text
except NoSuchElementException:
    num_of_pages = 1

extracted_products = []
for i in range(1,int(num_of_pages)+1):
    new_URL = URL + "&page=" + str(i)
    driver.get(new_URL)
    products = driver.find_elements(By.CSS_SELECTOR, CSS_PRODUCT)
    for product in products:
        product_data = {
            "Name" : product.find_element(By.CSS_SELECTOR, CSS_NAME).text,
            "Location": product.find_element(By.CSS_SELECTOR, CSS_LOCATION).text,
            "Info" : product.find_element(By.CSS_SELECTOR, CSS_INFO).text,
            "URL" : product.find_element(By.CSS_SELECTOR, CSS_URL).get_attribute("href")
        }

        price = product.find_element(By.CSS_SELECTOR, CSS_PRICE).text.replace(".","")
        product_data["Price"] = price
        if price.endswith("din"):
            product_data[f"Price in RSD as of {today}"] = float(price.removesuffix("din"))
        else:
            product_data[f"Price in RSD as of {today}"] = float(price.removesuffix("€")) * exchange_rate

        try:
            _ = product.find_element(By.CSS_SELECTOR, CSS_EXCHANGE_PRODUCT).text
            product_data["Exchange"] = "Yes"
        except NoSuchElementException:
            product_data["Exchange"] = "No"

        extracted_products.append(product_data)

print("Finished scraping at " + datetime.now().strftime("%H:%M:%S"))
csv_file = "products.csv"

with open(csv_file, mode="w", newline="\n", encoding="utf-8") as file:
    writer = csv.DictWriter(file,fieldnames=["Name","Price",f"Price in RSD as of {today}","Exchange","Location","Info","URL"])
    writer.writeheader()
    writer.writerows(extracted_products)

print(f"Data has been written to {csv_file}")

driver.quit()