import requests
from bs4 import BeautifulSoup

########################################### Helper functions to get the trending T-shirt names#########################################################

# This function concatenate a list of T-shirt names into a string and removes extra spaces
def list_to_string(word_list):
    string = []
    for word in word_list:
        string.append(word)
    
    string = ' '.join(string)
    string = " ".join(string.split()) #removes extra spaces (in each names' end)
    return string


# This function converts input text in to a list which contains each input word (first removes any extra space)
def string_to_list_handler(input_string):
    input_string = " ".join(input_string.split()) #removes extra spaces (in each names' end)
    input_list = input_string.split()
    return input_list

# This function stripes the style in the T-shirt name (This function targets the name in lowercases)
def style_remover(string):
    string = string.lower()
    styles = ['active t-shirt', 'baseball ¾ sleeve t-shirt', 'chiffon top',
          'classic t-shirt','essential t-shirt','fitted t-shirt',
          'fitted scoop t-shirt','fitted v-neck t-shirt','graphic t-shirt',
          'long t-shirt','long sleeve t-shirt','premium t-shirt',
          'premium scoop t-shirt','relaxed fit t-shirt','sleeveless top',
          'tri-blend t-shirt','v-neck t-shirt','t-shirt','shirt']
    for item in styles:
        string = string.replace(item,'')
    return string

# This function removes any article in the T-shirt's name
def article_remover(string):
    articles = ['the','a','an']
    string_list = string_to_list_handler(string)
    for item in articles:
        if item in string_list:
            string_list.remove(item)
    string = list_to_string(string_list)

    return string

# This function takes a list of words and returns a combo list which contains the single AND
# plural form of those words
def plural_list_converter(single_list):
    combo_list = []
    for i in single_list:
        modifiedWord = ""
        if i.endswith("y"):
            modifiedWord = i[0:len(i) -1] + "ies"
        elif i.endswith("f"):
            modifiedWord = i[0:len(i) -1] + "ves"
        elif i.endswith("f"):
            modifiedWord = i[0:len(i) -2] + "ves"
        elif i.endswith("s") or i.endswith("x") or i.endswith("z") or i.endswith("ch") or i.endswith("sh"):
            modifiedWord = i + "es"
        elif i.endswith("us"):
            modifiedWord = i[0:len(i) -2] + "i"
        else:
            modifiedWord = i + "s"
       
        combo_list.append(i)
        combo_list.append(modifiedWord)
        
    return combo_list

# This function takes in two strings, and removes any word the target string has which is also in the search term string
# This fuction also moves the search terms in plural
def search_word_remover(search_term, target_string):
    search_term_list = string_to_list_handler(search_term)
    search_term_combo_list = plural_list_converter(search_term_list) # This list includes the search terms' plural forms
    target_string_list = string_to_list_handler(target_string)
    for word in target_string_list:
        if word in search_term_combo_list:
            target_string_list.remove(word) # remove the word from the list
    
    output_string = list_to_string(target_string_list)
    
    return output_string

# This function stripes any non-alphanumeric space characters a T-shirt name might have (excluding spaces)
def name_format(string):
    values = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
    for item in string:
        if item not in values:
            string = string.replace(item, "")
    string = " ".join(string.split())
    return string

# This function outputs the url on Redbubble given a search term
def get_url_rb(search_term):
    url = (f'https://www.redbubble.com/shop/?iaCode=u-tees&query={search_term}&sortOrder=trending').replace(' ','%20')
    return url

# This function grabs the relevant data given an url
def get_data(url):
    headers = {'User-Agent': 'asxcv'} # This is an arbitrary value
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# This function returns a namelist which contains T-shirts name (after removing T-shirt styles and any articles in the name)
def parse(soup):
    # testing if any valid result can be found on redbubble
        not_found = 'NOT FOUND'
        result = soup.find('span', {'class': 'styles__box--2Ufmy styles__text--23E5U styles__display3--1CDP5 styles__display-block--3kWC4'})
        if result is not None :
            return not_found

        else:
            namelist = []
            results = soup.find_all('a', {'class': 'styles__link--3QJ5N'})
            for item in results:
                item_name = item.find('span',{'class': 'styles__box--2Ufmy styles__text--23E5U styles__display6--3wsBG styles__nowrap--33UtL styles__display-block--3kWC4'}).text
                item_name = style_remover(item_name) # This removes the style suffix on T-shirts' names
                item_name = name_format(item_name) # This removes any non-alphanumeric space characters a T-shirt name might have (excluding spaces)
                item_name = article_remover(item_name) # This removes any articles in the T-shirt's name
                namelist.append(item_name)
    
            return namelist


def counter(string):
    string = " ".join(string.split())
    string = string.lower()
    words = string.split(' ')
    count = dict()

    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

    most_word = max(count.values(), key = lambda x: int(x))

    most_word_array= [key for key in count if int(count[key]) == most_word]

    count = sorted(count.items(), key=lambda x: x[1], reverse=True) # Sorting dictionary count: this sorts the values in count in decending order

    if count[0][1] == count[-1][1]: # if the words all have the same counts
        no_trend = 'NO TREND'
        return no_trend
    
    else:
        
        trend_word = list_to_string(most_word_array)

        return trend_word

#######################################################################################################################################################

# This is the actual function which returns the names of the trending T-shirts in a string
def get_trend_words(search_term):
    url = get_url_rb(search_term)
    soup = get_data(url)
    namelist = parse(soup)
    name_string_all = list_to_string(namelist) # The T-shirt names are now ALL in a string
    name_string_excl_search = search_word_remover(search_term,name_string_all) # This removes the search words from the names string
    trend_word = counter(name_string_excl_search)

    return trend_word