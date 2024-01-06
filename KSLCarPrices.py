from selenium import webdriver
from selenium.webdriver.common.by import By
import fnmatch
import time
import pandas as pd
import sqlite3


carlistings = []
conn = sqlite3.connect('carprices.sqlite')


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

options = webdriver.FirefoxOptions()
specs = ["makeYear", "transmission", "make ", "liters", "model", "cylinders", "trim", "fuel", "body", "numberDoors", "cabSize", "numberOfSeats", "bedSize", "mileage", "exteriorCondition", "vin", "interiorCondition", "titleType", "drive", "paint", "dealerLicense", "upholstery", "stockNumber", "price"]
cars = []

def is_error_page(driver):
    try:
        error_div = driver.find_element(By.XPATH, "//div[contains(@class, 'Error')]")
        return True
    except:
        return False

for car in listings:
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(car)
        time.sleep(5)
        if is_error_page(driver):
            print(f"Error: This page is not valid {car}")
        else:
            driver.implicitly_wait(2)
            try:
                driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
                time.sleep(1)
            except:
                time.sleep(5)
                driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
                time.sleep(1)
            driver.execute_script("window.scrollTo(0, window.innerHeight / 1.8);")
            driver.implicitly_wait(2)
            SeeMore = driver.find_elements(By.XPATH, ".//button[text()='See More']")
            SeeMore[-1].click()
            driver.implicitly_wait(2)
            car = []
            for spec in specs:
                try:
                    if spec == 'price':
                        xpath = "//h2[contains(@class , 'ercllS') and contains(@style, 'color')]"
                        price = driver.find_element(By.XPATH, xpath)
                        car.append(price.text)
                        print("Price")
                    else:
                        xpathexp = f"//div[contains(@class, '{spec}')]/div[contains(@class, 'value')]//p[contains(@class, 'Typography__variantProp-sc-5cwz35-0') and contains(@class, 'kMOSqH')]"
                        info = driver.find_element(By.XPATH, xpathexp)
                        car.append(info.text)
                except Exception as e:
                    xpathexpa = f"//div[contains(@class, '{spec}')]/div[contains(@class, 'value')]//a[contains(@class, 'Typography__variantProp-sc-5cwz35-0') and contains(@class, 'kMOSqH')]"
                    info = driver.find_element(By.XPATH, xpathexpa)
                    car.append(info.text)
            print(car)
            cars.append(car)
    except Exception as e:
        print("ERROR")
    finally:
        driver.quit()


df = pd.DataFrame(cars, columns = specs)
df.to_sql('cars', conn, if_exists='replace')


