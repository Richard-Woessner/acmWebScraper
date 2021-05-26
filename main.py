from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv

table = []
with open('backup/f12.csv', newline='') as f:
    reader = csv.reader(f)
    #table = list(reader)

driver = webdriver.Chrome()
driver.get("https://dl.acm.org/conference/cpr/proceedings")
elem = driver.switch_to.active_element
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="conference-C-0"]/div/span/span').click()
test = driver.find_elements_by_xpath('//*[@id="conference-C-0"]/div/ul/li')
print(test)

links = []
i = 0
for x in test:
    links.append(x.find_element_by_tag_name('a').get_attribute('href'))

for index, link in enumerate(links):
    if (index < 0):
        continue
    print(link)
    print(str(index)+' / '+str(len(links)))
    # open tab
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(link)
    # open all
    lists = driver.find_elements_by_xpath(
        '//*[@id="pb-page-content"]/div/main/div[4]/div/div[2]/div[1]/div/div[2]/div/div/div')
    for x in lists:

        drop = x.find_element_by_tag_name('a')
        if (drop.get_attribute('aria-expanded') == 'false'):
            drop.click()
        else:
            continue

        time.sleep(2.0)

    awards = driver.find_elements_by_class_name('issue-item__content')

    for index, award in enumerate(awards):
        print(str(index) + ' / ' + str(len(awards)))
        try:
            title = award.find_element_by_class_name('issue-item__title').find_element_by_tag_name('a').text
        except:
            title = ''
        try:
            author = award.find_element_by_tag_name('ul').find_element_by_tag_name('a').get_attribute('title')
        except:
            author = ''
        spans = award.find_element_by_class_name('issue-item__detail').find_elements_by_tag_name('span')
        date = spans[0].text
        doi = spans[2].text
        try:
            ab = award.find_element_by_tag_name('p')
            syn = ab.text
            if ab.find_element_by_tag_name('a').text == '… (More)':
                print('true')
                newTab = award.find_element_by_tag_name('a').get_attribute('href')
                print(newTab)
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(newTab)
                time.sleep(2.0)
                syn = driver.find_element_by_class_name('abstractSection').find_element_by_tag_name('p').text
                print(syn)
                driver.close()
                time.sleep(2.0)
                driver.switch_to.window(driver.window_handles[0])


        except:
            syn = ''
        row = [title, author, date, doi, syn]
        table.append(row)
        print(title)

    df = pd.DataFrame(table, columns=['title', 'author', 'date', 'doi', 'ab'])
    df.to_csv('f' + str(index) + '.csv', index=False)

    i = i + 1
