from algorithm.redbubble_scrape import get_trend_words, name_format
from algorithm.freepik_scrape import get_trend_image_fp
from algorithm.unsplash_scrape import get_trend_image_unsplash

# This function takes an input search term and outputs an image url
def get_image_url(search_term):
    imagelist = []
    search_term = name_format(search_term) # This formats the search term
    trend_words = get_trend_words(search_term)
    img_search_term = trend_words + ' ' + search_term # This is the output trend word/s
    #print(output_term) #这个search出来的term可保留作为sales predict时需要的term, 也可以用图片搜出来的title，也可以两者都用（先用title，搜不出再用这个）
        ##image_url, image_name = get_trend_image(search_term)
    imagelist_fp = get_trend_image_fp(img_search_term)
    imagelist_unsplash = get_trend_image_unsplash(img_search_term)

    for item in imagelist_fp:
        imagelist_unsplash.append(item)
    
    imagelist = imagelist_unsplash

    return imagelist, trend_words, search_term


############################ TESTING: getting image url ##################################################
""" search_term = 'cat'
imagelist, trend_words = get_image_url(search_term)
print(imagelist)
print(trend_words) """

