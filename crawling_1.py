from bs4 import BeautifulSoup
import requests
import warnings


#warning - ignore the warning coming up
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

#Bright data - used "unblocker" solution, Scraping browser api ( preventing the block from the website )
host = "brd.superproxy.io:22225"
user_name = "brd-customer-hl_dd579916-zone-unblocker"
password = "lbxa4gqxo6nn"
proxy_url = f"https://{user_name}:{password}@{host}"
proxies = {"https": proxy_url, "https": proxy_url}
print(proxy_url)

keyword = input("search the item : ")
# url = f"https://www.coupang.com/np/search?component=&q={keyword}" 

link_list = []
for page_num in range(1,2):
    print(f"<<<<<<<<<<<<<<<<{page_num}>>>>>>>>>>>>>>>>>>")

    url = f"https://www.coupang.com/np/search?q={keyword}&page={page_num}&listSize=36"
    print(url)
    print()

    # *verify=false can be ignored the SSl certificate

    response = requests.get(url, proxies=proxies, verify=False)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("[class=search-product]")

    print(len(items))

    for item in items:
        name = item.select_one(".name").text
        price = item.select_one(".price-value")
        if not price :
            continue
        link = f"https://coupang.com{item.a['href']}"

        link_list.append(link)

        print(f"{name} : {price.text}")
        print(link)
        print()

print(link_list)
print(len(link_list))


for url in link_list:
    response.encoding = 'utf-8'
    response = requests.get(url, proxies=proxies, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")    

    brand = soup.select_one(".prod-brand-name").text.strip()
    title = soup.select_one(".prod-buy-header__title").text.strip()

    prod_sale_price = soup.select_one(".prod-sale-price")
    prod_coupon_price = soup.select_one(".prod-coupon-price")

    print(f"브랜드: {brand}, 제품명: {title}")


