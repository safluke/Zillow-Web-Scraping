from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

GOOGLESHEET= "https://forms.gle/vt34jEEherDGQvHy5" 
ZILLOW = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C"usersSearchTerm"%3Anull%2C"mapBounds"%3A%7B"west"%3A-122.69219435644531%2C"east"%3A-122.17446364355469%2C"south"%3A37.703343724016136%2C"north"%3A37.847169233586946%7D%2C"isMapVisible"%3Atrue%2C"filterState"%3A%7B"fr"%3A%7B"value"%3Atrue%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%2C"fsbo"%3A%7B"value"%3Afalse%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"auc"%3A%7B"value"%3Afalse%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"pmf"%3A%7B"value"%3Afalse%7D%2C"pf"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B"max"%3A3000%7D%2C"price"%3A%7B"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%7D%2C"isListVisible"%3Atrue%2C"mapZoom"%3A11%7D'
retrieved=False
while retrieved==False: 

    response = requests.get(ZILLOW, headers=header)
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    div_class="StyledPropertyCardDataWrapper-c11n-8-69-2__sc-1omp4c3-0 KzAaq property-card-data"
    div_class2="StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 kJFQQX"
    
    articles = soup.find_all(name = "a", class_="StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 dZxoFm property-card-link")
    
    #articles=soup.select(".StyledPropertyCardDataWrapper-c11n-8-69-2__sc-1omp4c3-0 KzAaq property-card-data ")


    addresses=[]
    prices=[]
    links=[]
    for i in articles:
        
        
        addresses.append(i.text)
        
        if "http" not in i.get("href"):
            links.append(f'https://www.zillow.com{i.get("href")}')
        else:
            links.append(i.get("href"))
        price= (i.next_element.next_element.next_element.next_element.text)
        if "+" in price:
            prices.append(str(price).split("+")[0])
        else: 
            prices.append(str(price).split("/")[0])
        
            
    print (addresses,prices,links)
    print (len(addresses),len(prices),len(links))
    
    if addresses== []:
        time.sleep(2)
        retrieved=False
    else:
        retrieved=True
    
chrome_driver_path = r"C:\Users\Saf_2\.spyder-py3\Python Projects\Web Scraping Selenium\chromedriver.exe"
driver=webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(GOOGLESHEET)


for i in range(len(addresses)):
    time.sleep(2)
    in_address =  driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    in_price= driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    in_link= driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button= driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    in_address.send_keys(addresses[i])
    in_price.send_keys(prices[i])
    in_link.send_keys(links[i])
    time.sleep(2)
    submit_button.click()
    return_button=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    return_button.click()