import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import spacy

nlp = spacy.load("en_core_web_sm") # This is the language module which has been pre-installed
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
pagination = 3

# This function calculates the text similarity on two strings
def text_similarity(given,string):
    given = nlp(given)
    string = nlp(string)
    similarity = given.similarity(string)
    return similarity

# This function deals with pagination (current pagination is 3) and outputs a list of urls
def get_url_list_etsy(search_term):
    url_list = []
    for page in range (pagination):
        page = page + 1
        url = (f'https://www.etsy.com/uk/search?q={search_term}+t-shirt&is_content_partial=true&explicit=1&order=most_relevant&page={page}&ref=pagination').replace(' ','+')
        url_list.append(url)

    return url_list

# This function gets web data on a given url
def get_data(url):
    r = requests.get(url, headers = headers)
    status = r.status_code
    if status == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    else:
        return None

# This function scrapes web data and output sales and product data
def parse(soup, search_term, sales_container, product_container):
    search_term = search_term + ' ' + 'T-shirt'

    results= soup.find('ul', {'class': 'wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container'}).find_all('li')

    for item in results:
    
        try:
            page_link_url = item.find('a')['href']
            in_page_request = requests.get(page_link_url, headers = headers)
            in_page_soup = BeautifulSoup(in_page_request.text, 'html.parser')
            
            sales = in_page_soup.find('span',  {'class': 'wt-text-caption'}).text

            try:
                sales_figure = int(sales.replace(',','').replace(' sales',''))
                sales_container.append(sales_figure)

                try:
                    name = item.find('img')['alt']
                    image_url = item.find('img')['src']
                    if image_url is not None:
                        if name is not None:
                            similarity = text_similarity(search_term, name)
                            product = {
                                'similarity': float(similarity),                               
                                'title' : name,
                                'image': image_url,
                                'link': page_link_url,
                                'sales' : sales_figure,
                            }

                            product_container.append(product)
                            
                except:
                    pass

            except:
                pass
        except:
            pass
    
# This is the actual function which output average sales and the products (sorted in decending similarity)
## and it is an indicator of how successful the generated design would be    
def get_sales_info(search_term):
    url_list = get_url_list_etsy(search_term)
    sales_container = [] # This will contain valid scrapped sales data
    product_container = [] # This will contain valid scrapped products
    total_sale = 0
    avg_sale = 0
    for url in url_list:
        soup = get_data(url)
        if soup is not None:
             parse(soup, search_term, sales_container, product_container) # pass in 4 variables (want this function to modify the last 3 variables)
    
    if product_container is not None:
        product_container = list({v['link']:v for v in product_container}.values()) # only products with different page/link are retained in the product_container
        product_container = list({v['title']:v for v in product_container}.values())
        product_container = sorted(product_container, key = itemgetter('similarity'), reverse = True)
        if len(product_container) > 12:
            product_container = product_container[0:12] # This will only return the first 10 products
        for product in product_container:
            total_sale = total_sale + product['sales']
        avg_sale = int(total_sale / len(product_container))

    
    return avg_sale, product_container  # Note need to check if this avg_sale is 0

    


################################################### Testing #######################################

#print(get_url_list_etsy('funnt cat'))

""" search_term = 'black cat'
avg_sale, product_container = get_sales_info(search_term)


print(product_container)
print(avg_sale)
 """