from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fnmatch
import time
import pandas as pd
import sqlite3

carlistings = []
conn = sqlite3.connect('carprices.sqlite')
options = webdriver.FirefoxOptions()
specs = ["makeYear", "transmission", "make ", "liters", "model", "cylinders", "trim", "fuel", "body", "numberDoors", "cabSize", "numberOfSeats", "bedSize", "mileage", "exteriorCondition", "vin", "interiorCondition", "titleType", "drive", "paint", "dealerLicense", "upholstery", "stockNumber", "price"]
cars = []

for i in range(1,2):
    driver = webdriver.Chrome()
    url = f"https://cars.ksl.com/sitemap/srp-used?page={i}"
    driver.get(url)
    links = driver.find_elements(By.CLASS_NAME, "opened")
    for link in links:
        carlistings.append(link.text[5:-37])
    driver.quit()

listings = fnmatch.filter(carlistings, "https://cars.ksl.com/listing/???????")


# I Want to loop through this list of car listings, click on see more for the vehicle specs
# grab the info, and load it into a dataframe



def is_error_page(driver):
    try:
        error_div = driver.find_element(By.XPATH, "//div[contains(@class, 'Error')]")
        return True
    except:
        return False
driver = webdriver.Firefox(options=options)

for car in listings:
    try:
        driver.get(car)
        if is_error_page(driver):
            print(f"Error: This page is not valid {car}")
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
            driver.execute_script("window.scrollTo(0, window.innerHeight / 1.8);")
            SeeMore = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//button[text()='See More']")))
            SeeMore[-1].click()
            car = []
            for spec in specs:
                try:
                    if spec == "price":
                        price = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                        car.append(price.text)
                    else:
                        try:
                            xpathexp = f"//div[contains(@class, '{spec}')]/div[contains(@class, 'value')]//p[contains(@class, 'Typography__variantProp-sc-5cwz35-0') and contains(@class, 'kMOSqH')]"
                            info = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpathexp)))
                            car.append(info.text)
                        except Exception as e:
                            xpathexpa = f"//div[contains(@class, '{spec}')]/div[contains(@class, 'value')]//a[contains(@class, 'Typography__variantProp-sc-5cwz35-0') and contains(@class, 'kMOSqH')]"
                            info = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpathexpa)))
                            car.append(info.text)
                except:
                    print("Crust")
            cars.append(car)
    except Exception as e:
        print("ERROR")

driver.quit()


df = pd.DataFrame(cars, columns = specs)
df.to_sql('cars', conn, if_exists='replace')
