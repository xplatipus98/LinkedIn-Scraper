# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import creds
import pandas as pd
#Credentials
user=creds.username
passw= creds.password
num_pages=20
# defining new variable passing two parameters
#writer = csv.writer(open(parameters.file_name, 'wb'))

# writerow() method to the write to the file object
#writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])
#Remove Duplicate from list
def Remove(duplicate): 
    final_list = [] 
    if len(duplicate) > 1 :
        for num in duplicate: 
            if num not in final_list: 
                final_list.append(num) 
        return final_list
    else:
        return duplicate 
# To get Xpath_num
def Xpath_num(l):
    new=[]
    for i in range(len(l)):
        if i%2 ==0: 
            x=l[i]
            new.append(x)
    new = [int(s.split('r')[1]) for s in new]
    return new
#To get Xpath for name
def name_ember(l):
    x_path=[]
    for num in l:
        path='//*[@id="ember{}"]/span/span/span[1]'.format(num+5)
        x_path.append(path)
    return x_path
#To get Xpath for post
def post_ember(l):
    x_path=[]
    for num in l:
        path='//*[@id="ember{}"]/div/div[2]/p[1]'.format(num-1)
        x_path.append(path)
    return x_path

#To go to next page
def next_page(i):
    url='https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22636230%22%5D&page={}'.format(i+1)
    driver.get(url)
    return 0

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('C:\webdriver\chromedriver.exe')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_css_selector('#session_key')

# send_keys() to simulate key strokes
username.send_keys(user)

# sleep for 0.5 seconds
#sleep(0.5)
time.sleep(0.5)
# locate password form by_class_name
password = driver.find_element_by_css_selector('#session_password')

# send_keys() to simulate key strokes
password.send_keys(passw)
time.sleep(0.5)

# locate submit button by_xpath
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

# .click() to mimic button click
sign_in_button.click()
#time.sleep(5)
#Search Query
#Query= "Hastings Direct Insurance Company"
url='https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22636230%22%5D'
driver.get(url)
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ember44 > input')))
#search_bar=driver.find_element_by_css_selector('#ember44 > input')
#search_bar.send_keys(Query)
#time.sleep(0.5)
#search_bar.send_keys(u'\ue007')
# getting the info
time.sleep(5)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'name.actor-name' )))
time.sleep(0.5)
WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'subline-level-1.t-14.t-black.t-normal.search-result__truncate')))
driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/4));")
time.sleep(1)
driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/3));")
time.sleep(1)
driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
time.sleep(1)
driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*2/3));")
time.sleep(1)
driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
# Name
linkedin_name = driver.find_elements_by_class_name('name.actor-name')
linkedin_name = [name.text for name in linkedin_name]
print(linkedin_name)
print(len(linkedin_name))
# LinkedIn Profile Link
linkedin_profile = driver.find_elements_by_class_name('search-result__result-link.ember-view')
links = ([elem.get_attribute('href') for elem in linkedin_profile])
links=Remove(links)
print(links)
print(len(links))
#Position
linkedin_post = driver.find_elements_by_class_name('subline-level-1.t-14.t-black.t-normal.search-result__truncate')

position = [post.text for post in linkedin_post]
print(position)
print(len(position))
#remove unwanted
#remove= driver.find_element_by_
###################################################################
data=pd.DataFrame(columns=['Name','Position','LinkedIn Profile'])
i=1
for k in range(num_pages):
    local_data= pd.DataFrame(columns=['Name','Position','LinkedIn Profile'])
    time.sleep(2)
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'subline-level-1.t-14.t-black.t-normal.search-result__truncate')))
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/4));")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/3));")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*2/3));")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
    print('########################################################################################## Page {} ######################################################################################################'.format(i))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'search-result__result-link.ember-view')))
    linkedin_profile = driver.find_elements_by_class_name('search-result__result-link.ember-view')
    ids=[elem.get_attribute('id') for elem in linkedin_profile]
    #ids.sort()
    print(ids)
    print(len(ids))
    names=[]
    posts=[]
    link_ids=[]
    ember_num=Xpath_num(ids)
    for num in ember_num:
        Xpath_name='//*[@id="ember{}"]/span/span/span[1]'.format(num+5)
        Xpath_post='//*[@id="ember{}"]/div/div[2]/p[1]'.format(num-1)
        Xpath_links='//*[@id="ember{}"]'.format(num+4)


        try:
            name_elem= driver.find_element_by_xpath(Xpath_name)
            name = name_elem.text
            names.append(name)

            post_elem= driver.find_element_by_xpath(Xpath_post)
            post = post_elem.text
            posts.append(post)

            link_elem= driver.find_element_by_xpath(Xpath_links)
            link = link_elem.get_attribute('href')
        #   link=Remove(link)
            link_ids.append(link)       

        except: continue

    print(names)
    print(len(names))
    local_data['Name'] = names

    print(posts)
    print(len(posts)) 
    local_data['Position'] = posts

    print(link_ids)
    print(len(link_ids)) 
    local_data['LinkedIn Profile'] = link_ids
    data=pd.concat([data, local_data], ignore_index=True)
    next_page(i)
    time.sleep(1)
    i+=1
driver.quit()
print(data.shape)
print(data)
data.to_excel("Hastings Direct Data.xlsx")

