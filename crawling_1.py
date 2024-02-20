from bs4 import BeautifulSoup
import requests
import warnings
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
import time
import random
import csv


#warning - ignore the warning coming up
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

AUTH = 'brd-customer-hl_dd579916-zone-scraping_browser:5p6x8can0tvr'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

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
with open(f"coupang_{keyword}.csv," "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writer(["제품명", "가격", "링크"])
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
            else:
                price = price.text
            link = f"https://coupang.com{item.a['href']}"

            link_list.append(link)

            writer.writerow([name, price, link])

            print(f"{name} : {price}")
            print(link)
            print()

print(link_list)
print(len(link_list))


for url in link_list:
    response.encoding = 'utf-8' 

    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.implicitly_wait(5)
        driver.get(url)
        html = driver.page_source
        print(html)
        soup = BeautifulSoup(html, "html.parser")

    #text.strip() - remove the empty blank
        brand = soup.select_one(".prod-brand-name")
        brand = "" if not brand else brand.text.strip()

        title = soup.select_one(".prod-buy-header__title").text.strip()

        seller = soup.select_one(".prod-sale-vendor-name")
        seller = "로켓배송" if not seller else seller.text.strip()
        
        # seller = "로켓배송" if not seller else seller.text.strip()
        # 
        # if seller:
        #     seller = seller.text.strip()
        # else:
        #     seller = "로켓배송"

        prod_sale_price = soup.select_one(".prod-sale-price")
        prod_coupon_price = soup.select_one(".prod-coupon-price")

        if prod_sale_price:
            prod_sale_price = prod_sale_price.select_one(".total-price").text.strip()
        else:
            prod_sale_price= ""

        if prod_coupon_price:
            prod_coupon_price = prod_coupon_price.select_one(".total-price").text.strip()
        else:
            prod_coupon_price= ""

        print(url)
        print(f"브랜드: {brand}, 제품명: {title}, 현재 판매가: {prod_sale_price}, 회원 판매가 :{prod_coupon_price}")

        prod_option_item = soup.select(".prod-option_item")
        
        if prod_option_item:
            option_list = []
            for item in prod_option_item:
                title = item.select_one(".title").string.strip()
                value = item.select_one(".value").string.strip()
                option_list.append(f"{title}: {value}")
            prod_option_item = ",".join(option_list)
            print(prod_option_item)
        else:
            prod_option_item = ""
        
        #prod-description .prod-attr-item - The space in the middle is used 
        #to retrieve all the small classes within the large class.
        prod_description = soup.select(".prod-description .prod-attr-item")

        if prod_description:
            description_list = []
            for description in prod_description:
                description_list.append(description.string.strip())
            prod_description = ", ".join(description_list)
            print(prod_description)
        else:
            prod_description = "" 
        
        driver.find_element(By.NAME, "review").click()
        time.sleep(random.uniform(2,3))

        try:
            driver.find_element(By.CSS_SELECTOR, ".sdp-review_article_no-review--active")
            print("등록된 상품이 없습니다")
            print()

        except:
            review_btns = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticlePageBtn")
            if len(review_btns) == 0:
                reviews = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticleReviewList")
                print(f"상품평 총 {len(review_btns)} 페이지")
            else:
                print(f"상품평 총 {len(review_btns)} 페이지")   
            print()

            #collect all the rating, headline, and contents from the reviews
            
            data_page_num = 1
            while True:
                reviews = driver.find_elements(By.CSS_SELECTOR, ".sdp-review__article__list.js_reviewArticleReviewList")
                
                for e, review in enumerate(reviews, 1):
                    #user_name
                    try:
                        review_user_name = review.find_element(By.CSS_SELECTOR, ".sdp-review_article_list_info_user_name").text
                    except:
                        review_user_name = "없음"
                    #rating
                    try:
                        rating = review.find_element(By.CSS_SELECTOR, ".sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue").get_attribute("data-rating")
                    except:
                        rating = "없음"
                    #review_date
                    try:
                        review_date = review.find_element(By.CSS_SELECTOR, ".sdp-reveiw_article_list_info_product-info_reg-date").text
                    except:
                        review_date = "없음"
                    #product_info_name
                    try:
                        product_info_name = review.find_element(By.CSS_SELECTOR, ".sdp-review-article_list_info_product-info_name").text
                    except:
                        product_info_name = "없음"
                    #review_headline
                    try:
                        review_headline = review.find_element(By.CSS_SELECTOR, ".sdp-review_article_list_headline").text
                    except:
                        review_headline = "없음"
                    #reveiw_content
                    try:
                        review_content = review.find_element(By.CSS_SELECTOR, ".sdp-review__article__list__review__content.js_reviewArticleContent").text
                    except:
                        review_content = "없음"
                    
                    print(f"====={data_page_num}페이지 {e}번 리뷰 =====")
                    print(f"리뷰어: {review_user_name}")
                    print(f"평점: {rating} 작성일: {review_date}")
                    print(f"제품명: {product_info_name}")
                    print(f"제목 : {review_headline}")
                    print(f"본문 : {review_content}")

                    try:
                        survey = review.find_element(By.CSS_SELECTOR, ".sdp-review_article_list_survey").text
                        print()
                        print(f"{survey}")
                    except:
                        pass
                    print()
                
                data_page_num += 1
                if data_page_num > len(review_btns):
                    break

                review_btn = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticlePageBtn[data-page='{data_page_num}']")
                review_btn.click()
                time.sleep(random.uniform(2,3))
                
        print()



