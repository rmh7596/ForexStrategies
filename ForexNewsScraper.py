from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.edge.options import Options
from selenium.webdriver.safari.options import Options
from time import sleep

# Source: https://www.investing.com/economic-calendar/
edge_options = Options()
edge_options.add_argument("headless")

driver = webdriver.Safari(options=edge_options)
driver.get("https://www.investing.com/economic-calendar/")

this_week_btn = driver.find_element(By.ID, "timeFrame_thisWeek")
this_week_btn.click() # Naviate to this week

sleep(3) # Wait for page to get updated
for i in range(30): #Ensure we hit the bottom of the page
    sleep(0.25)
    driver.execute_script("window.scrollBy(0, window.innerHeight)", "")


table = driver.find_elements(By.ID, "economicCalendarData")
table_elem = table[0]
rows = table_elem.find_elements(By.TAG_NAME, "tr")

rows = rows[2:]
day_lst = []
days = []

for row in rows:
    row_data = row.find_elements(By.TAG_NAME, "td")

    if (len(row_data) > 2): #Will not trigger on headings
        time = row_data[0].text.strip()
        sentiment_text = row_data[2].get_attribute("title")
        country = row_data[1].text.strip()
        event_name = row_data[3].text.strip()
        day_lst.append((time,sentiment_text,country))
    else:
        new_day = row_data[0].text.strip()
        days.append(day_lst) # Append the old list
        day_lst = []
        day_lst.append(new_day) # Start the new one

days.append(day_lst) # To ensure Saturday is included

driver.quit()

del days[0] # Remove the first list
print(days)
