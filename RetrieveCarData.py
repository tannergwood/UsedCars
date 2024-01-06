from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sqlite3

url = 'https://cars.ksl.com/listing/8734950'
#driver = webdriver.Chrome()
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get(url)
time.sleep(3)
driver.implicitly_wait(2)
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
time.sleep(1)
driver.execute_script("window.scrollTo(0, window.innerHeight / 1.8);")
driver.implicitly_wait(2)
SeeMore = driver.find_elements(By.XPATH, ".//button[text()='See More']")
SeeMore[-1].click()
driver.implicitly_wait(2)
specs = ["makeYear", "transmission", "make ", "liters", "model", "cylinders", "trim", "fuel", "body", "numberDoors", "cabSize", "numberOfSeats", "bedSize", "mileage", "exteriorCondition", "vin", "interiorCondition", "titleType", "drive", "paint", "dealerLicense", "upholstery", "stockNumber", "price"]
cars = []
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


cars.append(car)
print(cars)
df = pd.DataFrame(cars, columns = specs)
print(df)
conn = sqlite3.connect('carsinformation.sqlite')
df.to_sql('practice', conn, if_exists='replace')
driver.quit()


