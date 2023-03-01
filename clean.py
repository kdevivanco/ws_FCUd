import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

class Webscrape():
    def __init__(self):
        self.api_key = 'RW3O9D54I6Y5N56OQPMMT0TV8F8EPNLV897KVNC8TX1ZXR5V579QCZ8OHLMRQJ80C1HT9D33UF4M34ZO'
        self.responses = []
        self.soups = []
    
    def scrape_coupon_page(self):
        running = True
        counter = 0
        max_retries = 3
        retries = 0
        while running:
            counter += 1

            url = f'https://couponscorpion.com/page/{counter}'
            
            print(f'Scrapping url {url}')

            response = requests.get(
                url ='https://app.scrapingbee.com/api/v1/',
                params={
                    'api_key': 'RW3O9D54I6Y5N56OQPMMT0TV8F8EPNLV897KVNC8TX1ZXR5V579QCZ8OHLMRQJ80C1HT9D33UF4M34ZO',
                    'url': url,
                },
            )
            print('Response HTTP Status Code: ', response.status_code)
            print(f'Scrapped page {counter}')

            if response.status_code == 500 and retries < max_retries:
                print(f'Retrying page {counter} after {response.status_code} error...')
                counter -=1
                retries += 1
                continue
            elif response.status_code == 500 and retries >= max_retries:
                print(f'Max retries reached for page {counter}. Moving to the next page...')
                continue
            else:
                retries = 0
            dates = []
            self.responses.append(response)
            soup = bs4.BeautifulSoup(response.text,"lxml")
            for element in soup.select('.date_ago'):
                dates.append(element.text)
                if '4 days ago' in element.text:
                    running = False
                    return counter
            new_list = [s.strip() for s in dates]
            print(new_list)
        
       
    @staticmethod
    def get_coupon_script(link):
        #This method takes the link of the individual page for each course and gets the script that generates the udemy target link 
        driver = webdriver.Chrome()
        driver.get(link)
        link_element = driver.find_element(By.CLASS_NAME, 'btn_offer_block.re_track_btn') 

        link_url = link_element.get_attribute('href')

        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()

        counter = 0
        for a in soup.select('.btn_offer_block'):
            print(a)
            return a['href'] #TARGET LINK! 
    
    @staticmethod
    def get_udemy_url(target_link):
        driver = webdriver.Chrome()

        driver.get(target_link)

        time.sleep(5) #gives the page 5 seconds to load and reset link if the coupon is invalid

        current_url = driver.current_url

        driver.quit()

        return (current_url)
    
    @staticmethod
    def extract_coupon_code(link):
        coupon_code_regex = r"/\?couponCode=([A-Z0-9]+)$"
        match = re.search(coupon_code_regex, link)
        if match:
            return match.group(1)
        else:
            return False
    
        
    @staticmethod
    def clean_df(self):
        self.df = df.drop(df[df['code'] == 0].index)
        return self.df
    
    
    def get_raw_data(self):
        titles = []
        links = []
        time_passed =[]
        coupon_codes = []
        for response in self.responses:
            soup = bs4.BeautifulSoup(response.text,"lxml")
            for element in soup.select('article.offer_grid h3 a'):
                titles.append(element.text)
            for image in soup.select('.img-centered-flex'):
                links.append(image['href'])
                coupon_codes.append(0)
            for element in soup.select('.date_ago'):
                time_passed.append(element.text)
                
        time_passed = [s.strip() for s in time_passed]
        data = {
            'date':time_passed,
            'title':titles,
            'link':links,
            'code':coupon_codes
        }

        df = pd.DataFrame(data)
        self.df = df 
    
    def execute(self)
        #1.  Open each link

        for n in range(self.df.shape[0]):
            post_link = self.df.iloc[n]['link']

            #2. Extract target link 
            target_link = cls.get_coupon_script(post_link)

            udemy_link = cls.get_udemy_url(target_link)


            #3. Check if valid
            if udemy_link == 'javascript:void(0)':
                continue

            if not cls.extract_coupon_code(udemy_link):
                continue
            else: #VALID COUPON CODE
                coupon_code = cls.extract_coupon_code(udemy_link)
                self.df.loc[n, 'code'] = coupon_code #save to the data frame

        cls.clean_df()

        print(df.shape)
        print(df.head)
        
        df.to_csv("scraped_data.csv", index=False)
