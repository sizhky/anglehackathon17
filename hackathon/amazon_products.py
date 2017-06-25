from amazon.api import AmazonAPI
import requests
import concurrent.futures
# import urllib.request

access_key = 'AKIAICKBWHEJRIVDWHUA'
secret_key = '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'
associate_tag = 'sagarpatel-20'

amazon = AmazonAPI(access_key, secret_key, associate_tag)

#products = amazon.search('Apparel',Keywords='blue shirt', SearchIndex='All')
products = amazon.search_n(60, Keywords='blue shirt', SearchIndex='All')


data = []
URLS = []

for i, product in enumerate(products):
    jsn = {}
    jsn['asin'] = product.asin
    jsn['price'] = product.formatted_price
    jsn['img'] = product.large_image_url
    URLS.append(jsn['img'])
    print(jsn['img'])
    jsn['page'] = product.detail_page_url
    data.append(jsn)
    try:
        with open('amazon_images/{}.jpg'.format(i), 'wb') as f:
            f.write(requests.get(jsn['img']).content)
    except:
        pass


# print(URLS)

# for i in URLS:


# def getimg(count):
#     localpath = 'amazon_images/{0}.jpg'.format(count)
#     urllib2.request.urlretrieve(URLS[count], localpath)
#     URLS[count] = localpath

# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
#     for i in range(50):
#         e.submit(getimg, i)
