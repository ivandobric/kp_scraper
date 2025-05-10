from selenium import webdriver
from selenium.common import NoSuchElementException
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

URL = "ENTER_URL_HERE"
driver.get(URL)

try:
    page_list = driver.find_element(By.CSS_SELECTOR,".Pagination_numbers__9OjwH").find_elements(By.TAG_NAME, "div")
    num_of_pages = page_list[-1].text
except NoSuchElementException:
    num_of_pages = 1

extracted_products = []
for i in range(1,int(num_of_pages)):
    URL += f"&page={i}"
    driver.get(URL)
    products = driver.find_elements(By.CSS_SELECTOR, ".AdItem_adHolder__CWcMj")
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