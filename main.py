from bs4 import BeautifulSoup
from urllib import request as rqst
import re
import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, json
from selenium.common.exceptions import WebDriverException

source = "https://www.racingpost.com"
driverlink = 'C:/Users/Dave/Desktop/chromedriver.exe'
MAX_THREADS = 3
pageTwoLinkList = []
pageTwoList = []
json_binding = []


def pageOne(pageurl):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driverlink, options=chrome_options)  # options=chrome_options
    driver.get(pageurl)
    driver.implicitly_wait(3)
    html = driver.page_source
    # pageurl = rqst.urlopen(pageurl)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', {'class': 'RC-runnerRowWrapper'})
    horsesData = []
    print(1)
    try:
        all_table_datas = table.findAll('div', {'class': 'RC-runnerRow'})
        for data in all_table_datas:
            try:
                horse_link = data.find('a', {'class': 'RC-runnerName'})['href']
                print(source + horse_link)
                pageTwoLinkList.append(source + horse_link)
            except:
                horse_link = "null"
    except Exception as e:
        print(e)


def pageTwo(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(driverlink, options=chrome_options)  # options=chrome_options
    while True:
        driver.get(url)
        driver.implicitly_wait(5)
        html = driver.page_source
        # content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "ui-table hp-formTable ui-table_type1 ui-table_sortable"}).find("tbody", {
            "class": "ui-table__body"})
        if table != None:
            break
        else:
            print("Loop")
            continue
    try:
        allRow = table.findAll("tr", {"class": "ui-table__row"})
        print(len(allRow))
    except Exception as e:
        print(e)
    for row in allRow:
        try:
            Scrapedurl = row.find("a", {"class": "ui-link ui-link_table js-popupLink"})['href']
        except Exception as e:
            continue
        print(source + Scrapedurl)
        pageTwoList.append(source + Scrapedurl)


def finalPage(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(driverlink, options=chrome_options)
    for i in range(0, 100):
        driver.get(url)
        driver.implicitly_wait(5)
        html = driver.page_source
        # content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "rp-horseTable__table ng-scope"})
        if table != None:
            # print(table)
            print("ok")
            break
        else:
            print("Final Page Loop")
            continue
    try:
        for i in range(0, 5):
            winning_time = soup.find('div', {'class': 'rp-raceInfo'}).findAll('li')
            if len(winning_time) != 0:
                if len(winning_time[0].findAll('span', {'class': 'rp-raceInfo__value'})) > 3:
                    target_wining_time = winning_time[0].findAll('span', {'class': 'rp-raceInfo__value'})[2]
                    target_wining_time = re.sub(r"\s", "", target_wining_time.get_text(strip=True))
                    break
                else:
                    target_wining_time = winning_time[0].findAll('span', {'class': 'rp-raceInfo__value'})[1]
                    target_wining_time = re.sub(r"\s", "", target_wining_time.get_text(strip=True))
                    break
            else:
                continue
    except Exception as e:
        print(e)
        target_wining_time = "null"
    print(target_wining_time)
    try:
        for i in range(0, 5):
            time = soup.find('span', {'class': 'rp-raceTimeCourseName__time'})
            if time != None:
                time = time.get_text(strip=True)
                break
            else:
                continue
    except Exception as e:
        print(e)
        time = "null"
    print(time)

    # Class
    try:
        for i in range(0, 5):
            Class = soup.find('span', {'class': 'rp-raceTimeCourseName_class'})
            if Class != None:
                Class = Class.get_text(strip=True)
                Class = Class.replace("(", "").replace(")", "").replace("Class ", "")
                break
            else:
                continue
    except Exception as e:
        print(e)
        Class = 0
    print(Class)

    # Price
    try:
        for i in range(0, 5):
            price = soup.find('div', {'data-test-selector': 'text-prizeMoney'})
            if price != None:
                start = price.find('span', text='1st')
                end = price.find('span', text='2nd')
                content = ''
                item = start.nextSibling

                while item != end:
                    content += str(item)
                    item = item.nextSibling
                price = content.strip().replace("£", "").replace(",", "")
                break
            else:
                continue
    except Exception as e:
        print(e)

    print(price)
    # Distance
    try:
        for i in range(0, 5):
            dist = soup.find('span', {'class': 'rp-raceTimeCourseName_distance'})
            if dist != None:
                dist = dist.get_text(strip=True)
                break
            else:
                continue
    except Exception as e:
        print(e)
        dist = 0
    print(dist)

    # Going
    try:
        for i in range(0, 5):
            gng = soup.find('span', {'class': 'rp-raceTimeCourseName_condition'})
            if gng != None:
                gng = gng.get_text(strip=True)
                break
            else:
                continue
    except Exception as e:
        print(e)
        gng = "Nan"
    print(gng)

    # Course Name
    try:
        for i in range(0, 5):
            course_name = soup.find('a', {'class': 'rp-raceTimeCourseName__name'})
            if course_name != None:
                course_name = course_name.get_text(strip=True)
                break
            else:
                continue
    except Exception as e:
        print(e)
        course_name = "null"
    print(course_name)

    # Date
    try:
        for i in range(0, 5):
            date = soup.find('span', {'class': 'rp-raceTimeCourseName__date'})
            if date != None:
                date = date.get_text(strip=True)
                break
            else:
                continue
    except Exception as e:
        print(e)
        date = "null"
    print(date)
    try:
        for i in range(0, 5):
            print(i + 1)
            mainRow = table.findAll('tr', {'class': 'rp-horseTable__mainRow'})
            # print(len(mainRow))
            if len(mainRow) != 0:
                break
            else:
                continue
    except Exception as e:
        print(e)

    # Draw And Pos
    pos = 0
    draw = 0
    count = 1
    # KeyWords
    # rp-horseTable__pedigreeRow ng-hide
    # Top Speed
    keywords = soup.findAll('tr', {'class': 'rp-horseTable__commentRow'})
    """for keyword in keywords:
        print(keyword.get_text(strip=True))"""

    """keywords = "null"
    try:
        for i in range(0, 5):
            keywords = soup.find('tr', {'class': 'rp-horseTable__commentRow'})
            if keywords != None:
                keywords = keywords.get_text(strip=True)
            else:
                continue
    except Exception as e:
        print(e)
    print("keywords: ", keywords)"""
    c=0

    try:
        for eachRow in mainRow:
            eachKeyword = keywords[c].get_text(strip=True)

            print("Keyword: ",eachKeyword)
            c+=1
            try:
                for i in range(0, 5):
                    pos_draw = eachRow.find('td').find('span',
                                                       {'class': 'rp-horseTable__pos__number'}).get_text().split()
                    try:
                        pos = re.sub(r"\s+", "", pos_draw[0])
                    except Exception as e:
                        print(e)

                    try:
                        draw = re.sub(r"\s+", "", pos_draw[1])
                        draw = draw.replace("(", "")
                        draw = draw.replace(")", "")
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

            # Horse Name
            try:
                for i in range(0, 5):
                    horseName = eachRow.find('td', {'class': 'rp-horseTable__horseCell'}).find('div', {
                        'class': 'rp-horseTable__horse'}).find('a')
                    if horseName != None:
                        horseName = horseName.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
                horseName = "null"
            # SP
            try:
                for i in range(0, 5):
                    sp = eachRow.find('td', {'class': 'rp-horseTable__horseCell'}).find('span', {
                        'class': 'rp-horseTable__horse__price'})
                    if sp != None:
                        sp = sp.get_text(strip=True)
                        break
                    else:
                        continue
            except Exception as e:
                print(e)
                sp = "null"
            print(horseName, " ", sp)

            # Trainer and Jokey
            try:
                for i in range(0, 5):
                    trainer_jokey = eachRow.find('div',
                                                 {'class': 'rp-horseTable__human rp-horseTable__human_medium'}).findAll(
                        'a')
                    if trainer_jokey != None:
                        jokey = trainer_jokey[0].get_text(strip=True)
                        trainer = trainer_jokey[1].get_text(strip=True)
                        break
                    else:
                        continue
            except Exception as e:
                print(e)
                trainer = "null"
                jokey = "null"
            print(trainer, "  ", jokey)

            # Age
            try:
                for i in range(0, 5):
                    age = eachRow.find('td', {'class': 'rp-horseTable__spanNarrow rp-horseTable__spanNarrow_age'})
                    if age != None:
                        age = age.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
                age = "null"
            print("Age: ", age)

            # WGT
            wgt = "null"
            try:
                for i in range(0, 5):
                    wgtScrape = eachRow.find('td', {'class': 'rp-horseTable__spanNarrow rp-horseTable__wgt'})
                    if wgt != None:
                        wgt = wgtScrape.find('span', {'class': 'rp-horseTable__st'}).get_text(strip=True)
                        wgt += "-"
                        wgt += wgtScrape.find('span', {'data-test-selector': 'horse-weight-lb'}).get_text(strip=True)
                        # wgt = wgt.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
            print("WGT: ", wgt)
            OR = "null"

            # OR
            try:
                for i in range(0, 5):
                    OR = eachRow.find('td', {'class': 'rp-horseTable__spanNarrow'})
                    if wgt != None:
                        OR = OR.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
            print("OR: ", OR)

            # Top Speed
            top_speed = "null"
            try:
                for i in range(0, 5):
                    top_speed = eachRow.find('td', {'data-test-selector': 'full-result-topspeed'})
                    if top_speed != None:
                        top_speed = top_speed.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
            print("top_speed: ", top_speed)

            # RPR
            rpr = "null"
            try:
                for i in range(0, 5):
                    rpr = eachRow.find('td', {'data-test-selector': 'full-result-rpr'})
                    if rpr != None:
                        rpr = rpr.get_text(strip=True)
                    else:
                        continue
            except Exception as e:
                print(e)
            print("RPR: ", rpr)
            j = {
                "time": [time],
                "Class": [Class],
                "Distance": [dist],
                "GNG": [gng],
                "CourseName": [course_name],
                "date": [date],
                "pos": [pos],
                "draw": [draw],
                "horse_name": [horseName],
                "SP": [sp],
                "trainer": [trainer],
                "jokey": [jokey],
                "age": [age],
                "weight": [wgt],
                "Official_rating": [OR],
                "TS": [top_speed],
                "RPR": [rpr],
                "Price": [price],
                "keyword": [eachKeyword],
                "winning_time": [target_wining_time],
                "url": [url]
            }
            print(j)
            # if count == 1:
            #    df = pd.DataFrame(j)
            #    df.to_csv('newData.csv', mode='a', header=True)
            #    count += 1
            # else:
            df = pd.DataFrame(j)
            df.to_csv('newData.csv', mode='a', header=False)
            json_binding.append(j)
    except Exception as e:
        print(e)
    print(json.dumps(json_binding))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    past = time.time()

    # finalPage("https://www.racingpost.com/results/15/doncaster/2021-07-31/788255")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    #    executor.map(finalPage, jfile["urls"])
    #
    # with open('jfile.json', 'a') as outfile:
    #    json.dump(json_binding, outfile)
    baseurl = "/racecards/"
    """pagetwoTryurl = "https://www.racingpost.com/profile/horse/2677071/v-chevaliers/form"
    finalPageUrl = ["https://www.racingpost.com/results/7/brighton/2021-05-18/782782","https://www.racingpost.com/results/394/southwell-aw/2020-11-26/772627",
                    "https://www.racingpost.com/results/1079/kempton-aw/2020-07-15/761145",
                    "https://www.racingpost.com/results/1079/kempton-aw/2019-12-11/744722",
                    "https://www.racingpost.com/results/15/doncaster/2021-01-30/774570",
                    "https://www.racingpost.com/results/1079/kempton-aw/2021-02-24/776844"]

    threads = min(MAX_THREADS, len(finalPageUrl))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(finalPage, finalPageUrl)
    with open('jfile.json', 'a') as outfile:
        json.dump(json_binding, outfile)"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(driverlink, options=chrome_options)  # options=chrome_options
    while True:
        driver.get(source + baseurl)
        driver.implicitly_wait(5)
        html = driver.page_source
        # content = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        allSections = soup.findAll("section", {"class": "ui-accordion__row"})
        if len(allSections) != 0:
            break
        else:
            print("Loop")
            continue
    # all = driver.find_elements_by_class_name("ui-accordion__row")
    print(len(allSections))
    racesurlList = []
    resultInJson = []
    for section in allSections:
        races = section.find("div", {"class": "RC-meetingList"}).findAll("div", {"class": "RC-meetingItem"})
        for race in races:
            if race != None:
                page = source + race.find('a')['href']
            racesurlList.append(page)

    # all urls in resulturlList
    print(len(racesurlList))
    threads = min(MAX_THREADS, len(racesurlList))
    # pageOne(racesurlList[0])
    print(racesurlList)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(pageOne, racesurlList)

    print("PageTwo Link List: ",pageTwoLinkList)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(pageTwo, pageTwoLinkList)

    print("PageTwo List: ",len(pageTwoList))
    pageTwoUrlJson = {
        "urls": pageTwoList
    }
    with open('pageTwoUrlJson.json', 'a') as outfile:
        json.dump(pageTwoUrlJson, outfile)


    # Take Files then go for final datascraping
    # f = open("list", "r")
    # listOfFinalUrls = f.read().splitlines()
    threads = min(MAX_THREADS, len(pageTwoList))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(finalPage, pageTwoList)
    data = pd.read_csv('newData.csv')
    # print(data)

    """file = open('pageTwoUrlJson.json')
    jsonFile = json.load(file)
    # pageTwoList = jsonFile['urls']
    print(pageTwoList)
    threads = min(MAX_THREADS, len(pageTwoList))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(finalPage, pageTwoList)

    with open('jfile.json', 'a') as outfile:
        json.dump(json_binding, outfile)

    file = open('jfile.json')
    data = json.load(file)
    print(len(data))
    data_in_csv = pd.read_json('jfile.json')
    data_in_csv.to_csv('mainDataset.csv', index=None)"""

    print((time.time() - past) / 3600)
