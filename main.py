#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Prevents chrome from closing
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Opens Cookie Clicker URL
URL = "https://orteil.dashnet.org/experiments/cookie/"
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

#Brings the cookie button, the amount of money as str, the name and cost of upgrades, the lists to store the names and upgrades, and the affordable ones.
cookie = driver.find_element(By.CSS_SELECTOR, value="#cookie")
str_money = driver.find_element(By.CSS_SELECTOR, value="#money")
all_upgrades = driver.find_elements(By.CSS_SELECTOR, value="#store b")
name_upgrades = []
init_cost_upgrades = []
affordable_upgrades = []

#For each upgrade in upgrades...
for item in all_upgrades:
    #We remove the hyphen and convert each word to a list item.
    split_list = item.text.split(" - ")

    #Get the name and cost of the upgrade.
    name_list = split_list[0]
    cost_list = split_list[-1]

    #Adds the name and cost to the name_upgrades and init_cost_upgrades list respectively.
    name_upgrades.append(name_list)
    init_cost_upgrades.append(cost_list)

#Remove the last item of both lists.
name_upgrades.pop()
init_cost_upgrades.pop()

#Removes the comma within certain prices in init_cost_upgrades and adds it to cost_upgrades to prevent any error.
cost_upgrades = [item.replace(',', '') for item in init_cost_upgrades]

#Variables for 5 minutes and 5 seconds.
five_min = time.time() + 60*10
one_sec = time.time() + 60*(1/60)

#Wait one second before starting the loop. 
time.sleep(1)

#While true
while True:

    #Click the cookie
    cookie.click()
    
    #Convert the money to an integer
    no_str_money = str_money.text.replace(",", "")
    int_money = int(no_str_money)

    #For every second...
    test = 0
    if test == 5 or time.time() > one_sec:

        #For every price in cost_upgrades.
        for cost in cost_upgrades:

            #We check to see if the cost is less than or equal to the current money we have.
            if int(cost) <= int_money:

                #Then we append them to a list called affordable_upgrades.
                affordable_upgrades.append(int(cost))

                #Find the maximum price tag.
                max_upgrade = str(max(affordable_upgrades))

                #Find the name of the upgrade
                max_index = cost_upgrades.index(max_upgrade)
                max_name = name_upgrades[max_index]

                #Click on the specific upgrade to buy the upgrade.
                final_name = f"buy{max_name}"
                max_link = driver.find_element(By.ID, value=final_name)
                max_link.click()
                cookie.click()

            #And finally, reset the affordable_upgrades list.
            affordable_upgrades = []  

    #If five minutes has passed...     
    if time.time() > five_min:

        # We find the cookie/sec rate.
        cookie_per_sec = driver.find_element(By.CSS_SELECTOR, value="#cps").text

        #We quit the browser and print the cookie/sec.
        driver.quit()  
        print(cookie_per_sec)

        #And stop the program from running.
        break

    #Subtracts the variable to ensure that only when the time has exceeded, the loop will run.
    test = test - 1
