import requests
import bs4


class Webscrape():
    def __init__(self):
        self.api_key = 'RW3O9D54I6Y5N56OQPMMT0TV8F8EPNLV897KVNC8TX1ZXR5V579QCZ8OHLMRQJ80C1HT9D33UF4M34ZO'
        self.response = []
    
    def scrape_coupon_page(self):
        print()
        counter = 1
        for num in range(0,11):
            url = f'https://couponscorpion.com/page/{counter}'
            response = requests.get(
            url='https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': self.api_key,
                'url': url,  
                },

            )
            print('Response HTTP Status Code: ', response.status_code)
            #print('Response HTTP Response Body: ', response.content)

            self.response.append(response)
            counter +=1
        
        return True 
    
    
    def get_courses_url(self):
        for response in self.response:
            self.soup = bs4.BeautifulSoup(response.text,"lxml")
            for element in self.soup.select('article.offer_grid h3 a'):
                print(element.text)
            for image in self.soup.select('.img-centered-flex'):
                print(image['href'])
    