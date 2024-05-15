from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from time import sleep
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import selenium.common.exceptions

# Source: https://www.investing.com/economic-calendar/
days_final = []
app = Flask(__name__)

def scrapeRows(driver):
    driver.get("https://www.investing.com/economic-calendar/")
    print("Successfully got website")
    this_week_btn = driver.find_element(By.ID, "timeFrame_thisWeek")
    this_week_btn.click() # Naviate to this week

    sleep(3) # Wait for page to get updated
    for i in range(30): #Ensure we hit the bottom of the page
        sleep(0.25)
        driver.execute_script("window.scrollBy(0, window.innerHeight)", "")


    table = driver.find_elements(By.ID, "economicCalendarData")
    table_elem = table[0]
    rows = table_elem.find_elements(By.TAG_NAME, "tr")
    return rows


def parseRows(rows):
    days = []
    day_lst = []
    for row in rows:
        row_data = row.find_elements(By.TAG_NAME, "td")

        if (len(row_data) > 2): #Will not trigger on headings
            time = row_data[0].text.strip()
            sentiment_text = row_data[2].get_attribute("title")
            country = row_data[1].text.strip()
            event_name = row_data[3].text.strip()

            # Only want high volatility events
            if sentiment_text == "High Volatility Expected":
                # Also only want EUR/USD news
                if country == "USD" or country == "EUR":
                    day_lst.append([time])
        else:
            new_day = row_data[0].text.strip()
            days.append(day_lst) # Append the old list
            day_lst = []
            day_lst.append(new_day) # Start the new one
    days.append(day_lst) # To ensure Saturday is included
    return days

@app.route('/nextEventSoon', methods=['GET'])
def isTimeToBuy():
    current_time = datetime.now()
    for day in days_final:
        time_delta_in_mins = ((day-current_time).seconds)/60
        if time_delta_in_mins < 5:
            return {"buy":True}
    return {"buy":False}

@app.route('/getEventList', methods=['GET'])
def getEventList():
    return days_final

scheduler = BackgroundScheduler()
@scheduler.scheduled_job(IntervalTrigger(days=7))
def updateDayList():
    days_final.clear()
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    firefox_options.add_argument("-no-sandbox")
    print("Attempting to connect to remote")
    try:
        driver = webdriver.Remote(command_executor="https://standalone-firefox-calendar-scraper.apps.okd4.csh.rit.edu", options=firefox_options)
        driver.set_page_load_timeout(45)
        driver.implicitly_wait(45)
        print("Connected to driver:", driver)
        rows = scrapeRows(driver)[2:]
        days_lst = parseRows(rows)
        driver.quit()

        del days_lst[0] # Remove the first list
        days_lst_filtered = filter(lambda x: len(x) > 2, days_lst)
        days_lst_filtered = list(days_lst_filtered)
        for i in range(len(days_lst_filtered)):
            for j in range(1, len(days_lst_filtered[i])):
                days_lst_filtered[i][j][0] = days_lst_filtered[i][0] + " " + days_lst_filtered[i][j][0]
                days_final.append(days_lst_filtered[i][j][0])

        for i in range(len(days_final)):
            days_final[i] = datetime.strptime(days_final[i], '%A, %B %d, %Y %H:%M')
        return
    except selenium.common.WebDriverException as e:
        print("Webdriver exception")
        driver.quit()
        print(e.msg)
        sleep(30) # Wait and try again
        updateDayList()
    

if __name__ == "__main__":
    updateDayList()

    scheduler.start()
    
    app.run(host="0.0.0.0")
