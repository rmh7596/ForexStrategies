from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# Source: https://www.investing.com/economic-calendar/
edge_options = Options()
edge_options.add_argument("headless")

driver = webdriver.Edge(options=edge_options)
driver.get("https://www.investing.com/economic-calendar/")

table = driver.find_elements(By.ID, "economicCalendarData")
#print(table.text)
#table = table[1:]
print("Table is found")
print(table[0].text)
#for row in table:
#    print(row.text)

#print(table.find_element(By.ID, "theDay1699747200"))
#print(driver.find_element(By.CLASS_NAME, "calendar__print calendar__print--header"))

driver.quit()