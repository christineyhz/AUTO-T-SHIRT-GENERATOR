import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'asxcv'} # This is an arbitrary value

# This is the function which gives back url on given search terms
def get_url_unsplash(search_term):
    url = (f'https://unsplash.com/s/photos/{search_term}').replace(' ','-')
    return url


# This is the function which gets data on a given url
def get_data(url):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


# This function scrapes information on images
def parse(soup):
    imagelist = []
    no_result = soup.find('div',{'class': 'rfzWF'})
    if no_result is not None :
            return imagelist
    else:
        try: 
            results = soup.find_all('figure', {'itemprop': 'image'})
            for item in results:
                try:
                    image_link = item.find('img')['src']
                    name = item.find('img')['alt']

                    image = {
                        'image_link': image_link,
                        'name': name
                    }

                    imagelist.append(image)
                except:
                    pass
        except:
            pass 
    
    if imagelist is not None:
        if len(imagelist) > 10:
            imagelist = imagelist[0:10]
    
    return imagelist        


# This is the actual function which outputs imagelist (atmost 5 images) on a given search term, and will output empty imagelist if no results found
def get_trend_image_unsplash(search_term):
    url = get_url_unsplash(search_term)
    soup = get_data(url)
    imagelist = parse(soup)
    return imagelist


########################################################### TESTING ###################################################################################
""" search_term = 'cat'
imagelist = get_trend_image(search_term)
print(imagelist) 
 """