# Accessing the API explorer: https://developer.ebay.com/my/api_test_tool
# HTTP request headers: https://developer.ebay.com/api-docs/static/rest-request-components.html#marketpl

import requests

def get_ebay_info(base64): 
  productlist = []
  # This is the url which is show on the ebay developers program searchByImage's official webpage: https://developer.ebay.com/api-docs/buy/browse/resources/search_by_image/methods/searchByImage
  # This url can produce better result than https://api.ebay.com/buy/browse/v1/item_summary/search_by_image?&limit=3&sort=-price , which is given on the offical API developer

  url ='https://api.ebay.com/buy/browse/v1/item_summary/search_by_image?'

  # This is the header provided on the API Explorer, it is the HTTP header which is used to take call request
  headers = {
      "Authorization":"Bearer v^1.1#i^1#p^1#I^3#f^0#r^0#t^H4sIAAAAAAAAAOVYbWwURRjuXa81iK2BEEoaxeuCCaK7O/t1Hwt35tprbUlpC9fWWoO4tzvXW3q3u+zMcb2SSNNGIppgBKMEjSkUrP7R+EGigkGEYCqYoIlRDCoxkiDGD4yJmpDo3PVarpXw1Uts4v25zMw77zzPM+878+6AgfI5y7c2bv2jwnGLc3gADDgdDm4umFNedm9lqbO6rAQUGDiGB5YOuAZLz69ESjJhyWshskwDQXdfMmEgOdcZoFK2IZsK0pFsKEmIZKzKkdDqZplngGzZJjZVM0G5m8IBipMkKSpxgIOiz+8BpNOYcNluBihBArwEeU6IRj2CJHJkHKEUbDIQVgwcoHjA8zTw0by/nfPIoijzgJFEqZtyd0Ib6aZBTBhABXNo5dxcuwDq1ZEqCEEbEydUsCnUEGkNNYXrW9pXsgW+gnkZIljBKTS1VWdq0N2pJFLw6sugnLUcSakqRIhig+MrTHUqhybA3AT8nNIigD5PVFElVfHwXugtipQNpp1U8NVxZHt0jY7lTGVoYB1nrqUoUSO6Aao432ohLprC7uzfmpSS0GM6tANUfW3ooVBbGxWsi9s6wrpBWxkcNw26bW2Y1nzAKwBN4GhVUqLQ6/Xmlxn3lRd52jp1pqHpWcmQu8XEtZBghtOVEQqUIUatRqsdiuEsnkI734SCArFjJ/YwheNGdldhksjgzjWvrf/kbIxtPZrCcNLD9IGcQAFKsSxdo6YP5iIxHzx9KEDFMbZklk2n00xaYEy7h+UB4Niu1c0RNQ6TCjVum811Yq9fewKt56iokMxEuowzFsHSRyKVADB6qKDo4f2SmNd9Kqzg9N5/dRRwZqfmQ7HywxcTBejxcB7Rr2lAUIuRH8F8iLJZHDCqZOikYvdCbCUUFdIqibNUEtq6JgtSjBd8MUhrHn+MFv2xGB2VNA/NxSAEEEajqt/3/0mT6w30CFRtiIsV6cWJ8sZYV69Qh63kxlCEbcOox7C607ixoePBUK26YVW0o6PTb5sPIL6xI3C9uXBF8nUJnSjTTtYvmgDZXC+OCCbCUJsRvYhqWrDNTOhqZnZtsGBrbYqNMxGYSJCOGZEMWVZT0U7q4tC7oUPi5lgX9X76L+6mK7JC2YCdXayy8xFxoFg6k719GNVMsqZCyg5Wyea6pa/PoZ4Rb53UrLOKNSE5zlbXxotNJkeZQZtUxobITNmkzmZas9VXu9kLDXKbYdtMJKDdyc04m5PJFFaiCTjb0roIAa4rs+yq5Ui15vVzogfMiJeau0jXz7YjqYgHsSt4YwU1O/XbPliS+3GDjgNg0PGG0+EALLibWwJqyks7XKW3VSMdQ0ZXYgzSewzyzWpDphdmLEW3neWOx1bLaz4veE0YXgcWTb4nzCnl5hY8LoA7Lo+UcbdXVfA88PF+UpOLPOgGSy6PuriFrgXVR1DVlw1Dbx4pad+/6fSflx5tHomAikkjh6OsxDXoKOk/Xr751WVPd/GXDHfN0W/E3aN3Db330/cXnXf+Ftece395buPh8DP7a7sk9uEVi19csOpYz56qtyqPzBMOi2MHL4QrywdP/aCxIwdD6de6T+46+vZFpn/4qWcrv33lzEv1+46fG30kXcOdP7bu5Qsfn/WfHq7e8uGZruT898equN+bh9a18NUHF89d8uR33t0rT+79at4Ktk/Zt+qLqvjIia9vjTADLyxPDYWXjbpKdpwwLj4fL/s7/mvFfKnf52/e8O7rm9+pvwf81br9kz6fPzjqDO2S04d24HmDgzVjT+zcu2zLZ1vuW/r4R3sWfSD8fG50ZI8yduDT6kOn+reFWs9uW3j/AnE7z5768ez49v0DC7b9GOcRAAA=",
      "Content-Type":"application/json",
      "X-EBAY-C-MARKETPLACE-ID":"EBAY_GB",
      "X-EBAY-C-ENDUSERCTX":"affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>"
  }

  # This is the image to be searched, which is a Base64 image
  request_data={
    'image': base64
  }

  try: 
  # The request to fetch data on ebay's server
    response = requests.post(url, headers=headers, json=request_data)
    data = response.json()
  
    items = data.get('itemSummaries')
    if len(items) > 8:
      items = items[0:8] # This will return the first 10 results

    for item in items:
      product = {
        'image': item['image']['imageUrl'],
        'title': item['title'],
        'link': item['itemWebUrl']
      }

      productlist.append(product)
  
  except:
    pass

  return productlist
