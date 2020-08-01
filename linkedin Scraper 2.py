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
num_pages=3

#Remove Duplicate from list
def Remove(duplicate): 
    final_list = [] 
    if len(duplicate) > 1 :
        for num in duplicate: 
            if num not in final_list: 
                if num == url: continue
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
    url_next=url+'&page={}'.format(i+1)
    driver.get(url_next)
    return 0

# To process the raw strings and extract names
def process_name(l):
    final=[]
    for item in l:
        if item is '':continue
        else:
            x=item.split("\n")[0]
            if x is 'LinkedIn Member': continue
            final.append(x)
    final = Remove(final)
    return final

# To select alternate
def select_alternate(l):
    final=[]
    for i in range(len(l)):
        if i % 2 != 0 :
            final.append(l[i])
    return final

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
url='https://www.linkedin.com/search/results/people/?keywords=hastings%20mutual%20insurance%20company&origin=FACETED_SEARCH'
driver.get(url)


data=pd.DataFrame(columns=['Name','Position','LinkedIn Profile'])
i=1
for k in range(num_pages):
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
    local_data= pd.DataFrame(columns=['Name','Position','LinkedIn Profile'])
    print('########################################################################################## Page {} ######################################################################################################'.format(i))
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'subline-level-1.t-14.t-black.t-normal.search-result__truncate')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'search-result__result-link.ember-view')))
    time.sleep(0.5)
    # Name and Profile Link
    # LinkedIn Profile Link
    linkedin_name = []
    links = []
    linkedin_profile = driver.find_elements_by_class_name('search-result__result-link.ember-view')
    for elem in linkedin_profile:
        name= elem.text
        name= name.split("\n")[0]
        if name == 'LinkedIn Member' :
            link = "No Link"
        else:
            link =(elem.get_attribute('href'))
        linkedin_name.append(name)
        links.append(link)

    linkedin_name= select_alternate(linkedin_name)
    print(linkedin_name)
    print(len(linkedin_name))
    local_data['Name'] = linkedin_name

    links = select_alternate(links)
    print(links)
    print(len(links))
    local_data['LinkedIn Profile'] = links
    
    #Position
    linkedin_post = driver.find_elements_by_class_name('subline-level-1.t-14.t-black.t-normal.search-result__truncate')
    position = [post.text for post in linkedin_post]
    print(position)
    print(len(position))
    local_data['Position'] = position

    data=pd.concat([data, local_data], ignore_index=True)
    next_page(i)
    time.sleep(1)
    i+=1
driver.quit()
print(data)
print(data.shape)