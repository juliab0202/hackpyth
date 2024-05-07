from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

s = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=s)
website = "http://127.0.0.1:5000/login"
driver.get(website)

titles=""
passwords = ["sdjknfv", "iewf", "sdkjf", "pass"]

i=0
for passw in passwords:
    print("testing this password", passw)

    res = driver.find_elements(By.CLASS_NAME, "form-control")

    assert(len(res) == 2)

    res[0].clear()
    res[0].send_keys("Bloom")
    time.sleep(1)
    #loeschen
    res[1].clear()
    #reinschreiben
    res[1].send_keys(passw)

    #button holen
    but = driver.find_elements(By.CLASS_NAME, "btn")
    assert (len(but) == 1)
    but[0].click()

    print(driver.title)
    if driver.title != "Please sign in":
        print(f"Password is {passw}")
        break

driver.quit()

