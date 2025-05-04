from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

options = webdriver.ChromeOptions()
# Block images
options.add_argument("--blink-settings=imagesEnabled=false")
# Headless mode
options.add_argument("--headless=new")

driver = webdriver.Chrome(
    options=options
    )

URL = "ENTER URL HERE"
URL += "&page=1"
driver.get(URL)

products = driver.find_elements(By.CSS_SELECTOR, ".AdItem_adHolder__CWcMj")
extracted_products = []
for product in products:
    product_data = {
        "Name" : product.find_element(By.CSS_SELECTOR, ".AdItem_name__Knlo6").text,
        "Price" : product.find_element(By.CSS_SELECTOR, ".AdItem_price__SkT1P").text,
        "Info" : product.find_element(By.CSS_SELECTOR, ".AdItem_adInfoHolder__FYK1b p").text,
        "URL" : product.find_element(By.CSS_SELECTOR, ".Link_link__2iGTE.Link_inherit__fCY5K").get_attribute("href")
    }
    extracted_products.append(product_data)

csv_file = "products.csv"

with open(csv_file, mode="w", newline="\n", encoding="utf-8") as file:
    writer = csv.DictWriter(file,fieldnames=["Name","Price","Info","URL"])
    writer.writeheader()
    writer.writerows(extracted_products)

print(f"Data has been written to {csv_file}")

driver.quit()