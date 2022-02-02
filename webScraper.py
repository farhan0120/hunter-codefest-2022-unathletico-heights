from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
import threading
import csv

def partition(begin, end):
    CHROME_PATH = "ENTER YOUR CHROME PATH HERE"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=chrome_options)
    # driver = webdriver.Chrome(PATH)


    URL = "https://boardgamegeek.com/boardgame/"



    error_file = open("ENTER ERROR FILE PATH HERE", 'a')
    header = ["URL", "Number", "Error"]
    eWriter = csv.writer(error_file)
    eWriter.writerow(header)

    f = open("ENTER OUTFILE PATH HERE", 'a')
    header = ["Number", "Name", "Players", "Time", "Age", "Difficulty", "Rank", "Description"]
    writer = csv.writer(f)
    writer.writerow(header)
    data = []


    for i in range(begin, end):
        driver.get(URL + str(i))#get url
        try:
            if(driver.find_element_by_id("edit_name").text):
                writer.writerow([i,driver.find_element_by_id("edit_name").text, '--', '--', '--', '--', '--', driver.find_element_by_id("editdesc").text])
                print([i,driver.find_element_by_id("edit_name").text, '--', '--', '--', '--', '--', '--', driver.find_element_by_id("editdesc").text])
                continue
        except:
            pass

        data.append(i)
        #title
        try:
            data.append(driver.find_elements_by_xpath("//h1")[2].text)
        except Exception as e:
            data.append('--')
            errors = [URL+str(i), i, e]
            eWriter.writerow(errors)
            print(e)

        #players,time,age,difficulty
        try:
            info = driver.find_elements_by_class_name("gameplay-item-primary")
            for j in range(len(info)):
                if(j<len(info)-1):
                    data.append(info[j].text)
                else:
                    data.append(info[j].text.split(" ")[1] + "/5")

        except Exception as e:
            for i in range(4):
                data.append('--')
            errors = [URL+str(i), i, e]
            eWriter.writerow(errors)
            print(e)

        try:
            #rank
            data.append(driver.find_element_by_class_name("rank-number").text + "/21839")
            # data.append(info.text + "/21839")
        except Exception as e:
            data.append('--')
            errors = [URL+str(i), i, e]
            eWriter.writerow(errors)
            print(e)

        try:
            #description
            data.append(driver.find_element_by_xpath("//article").text)
        except Exception as e:
            data.append('--')
            errors = [URL+str(i), i, e]
            eWriter.writerow(errors)
            print(e)
        try:
            writer.writerow(data)
        except:
            pass
        data = []


if __name__ == '__main__':

    t1 = Process(target=partition, args=(1,10001))
    t2 = Process(target=partition, args=(10001,20001))
    t3 = Process(target=partition, args=(20001,30001))
    t4 = Process(target=partition, args=(30001,40001))
    t5 = Process(target=partition, args=(40001,50001))
    t6 = Process(target=partition, args=(50001,60001))
    t7 = Process(target=partition, args=(60001,70001))
    t8 = Process(target=partition, args=(70001,80001))
    t9 = Process(target=partition, args=(80001,90001))
    t10 = Process(target=partition, args=(90001,100001))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
