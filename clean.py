import requests
import bs4


class Webscrape():
    def __init__(self):
        self.api_key = 'RW3O9D54I6Y5N56OQPMMT0TV8F8EPNLV897KVNC8TX1ZXR5V579QCZ8OHLMRQJ80C1HT9D33UF4M34ZO'
        self.response = []
    
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
        
       
    
    
    def get_courses_table(self):
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
            for element in soup.select('.date_ago'):
                time_passed.append(element.text)
        time_passed = [s.strip() for s in time_passed]
        data = {
            'date':time_passed,
            'title':titles,
            'link':links
        }

        df = pd.DataFrame(data)
        self.df = df 