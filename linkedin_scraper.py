import csv
from parsel import Selector
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


writer = csv.writer(open('testing.csv', 'w'))  # preparing csv file to store parsing result later
writer.writerow(['name', 'job_title', 'schools', 'ln_url'])

driver = webdriver.Chrome('D:\Linkdin_Scraper\linkedin_scraper\chromedriver_win32\chromedriver.exe')
time.sleep(2)
driver.get('https://www.linkedin.com')
time.sleep(5)

driver.find_element_by_xpath('//a[text()="Sign in"]').click()
time.sleep(5)
username_input = driver.find_element_by_name('session_key')
username_input.send_keys('guessme648@protonmail.com')

password_input = driver.find_element_by_name('session_password')
password_input.send_keys('heyyouitsnotme@123')


# click on the sign in button
# we're finding Sign in text button as it seems this element is seldom to be changed
driver.find_element_by_xpath('//button[text()="Sign in"]').click()

driver.get('https://www.google.com/')

search_input = driver.find_element_by_name('q')
# let google find any linkedin user with keyword "python developer" and "San Francisco"
search_input.send_keys('site:linkedin.com/in/ AND "python developer" AND "San Francisco"')

search_input.send_keys(Keys.RETURN)
my_list = []

for i in range(2):
    profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
    for profile in profiles:
        my_list.append(profile.get_attribute('href'))
        print(i)

    driver.find_element_by_xpath('//*[(@id="pnnext")]').click()


# visit each profile in linkedin and grab detail we want to get
for profile in my_list:
    time.sleep(1)
    url = str(profile)
    driver.get(url)

    try:
        sel = Selector(text=driver.page_source)
        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
        job_title = sel.xpath('//h2/text()').extract_first().strip()
        schools = ', '.join(
            sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        # location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        ln_url = driver.current_url

    except:
        print('failed')

    # print to console for testing purpose
    print('\n')
    print(name)
    print(job_title)
    print(schools)
    # print(location)
    print(ln_url)
    print('\n')
    writer.writerow([name, job_title, schools, ln_url])


driver.quit()
