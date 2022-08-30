import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from algorithm.redbubble_scrape import name_format

headers = {'User-Agent': 'asxcv'} # This is an arbitrary value

def get_url_fp(search_term):
    url = (f'https://www.freepik.com/search?format=search&query={search_term}&selection=1').replace(' ','%20')
    return url

def get_data(url):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    imagelist = []
    results = soup.find_all('figure', {'class': 'showcase__item js-detail-data caption'})
    
    for item in results:
        page_link_url = item.find('a')['href']
        in_page_request = requests.get(page_link_url, headers = headers)
        in_page_soup = BeautifulSoup(in_page_request.text, 'html.parser')
        try:
            in_page_result_data_likes= in_page_soup.find('div', {'class': 'detail'})['data-likes']
        except:
            in_page_result_data_likes = 0
        
        try:
            in_page_result_data_download= in_page_soup.find('div', {'class': 'detail'})['data-downloads']
        except:
            in_page_result_data_download = 0

        total = int(in_page_result_data_likes) + int(in_page_result_data_download)

        name = item.find('img')['alt']

        name = name_format(name)

        image = {
            'total': total,
            'page_link_url': page_link_url,
            'name': name,
            'image_link': in_page_soup.find('div', {'class': 'detail'})['data-image'],
            'download': in_page_result_data_download,
            'likes': in_page_result_data_likes
            
        }
        imagelist.append(image)
    
    imagelist = sorted(imagelist, key=itemgetter('total'), reverse=True) # This sorts the image list according to the total downloads and likes
    return imagelist

# This function returns the url of the image which has the highest download and like number given a search word
def get_trend_image_fp(search_term):
    imagelist = []
    url = get_url_fp(search_term)
    soup = get_data(url)
    imagelist = parse(soup)
    if imagelist is not None:
        #image_url = imagelist[0]['image_link']
        #image_name = imagelist[0]['name']
        if len(imagelist) > 10:
            imagelist = imagelist[0:10]
    
        #return image_url, image_name
    
    return imagelist


################################ Testing #####################################################
#print(get_trend_image_fp('funny cat'))