from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
import time
import random

AUTH = 'brd-customer-hl_dd579916-zone-scraping_browser:5p6x8can0tvr'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.implicitly_wait(5)
        driver.get('https://www.coupang.com/vp/products/7692638421?itemId=21283393377&vendorItemId=88332745751&q=%EB%85%B8%ED%8A%B8%EB%B6%81&itemsCount=36&searchId=e9cab9e315c149658d7a439689e0a050&rank=73&isAddedCart=')
        # print('Taking page screenshot to file page.png')
        # driver.get_screenshot_as_file('./page.png')
        # print('Navigated! Scraping page content...')
        # html = driver.page_source
        # print(html)
        time.sleep(random.uniform(2,3))
        driver.find_element(By.NAME, "review").click()
        time.sleep(random.uniform(2,3))

        try:
            driver.find_element(By.CSS_SELECTOR, ".sdp-review_article_no-review--active")
            print("등록된 상품이 없습니다")
            print()

        except:
            review_btn = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticlePageBtn")
            if len(review_btn) == 0:
                reviews = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticleReviewList")
                print(f"상품평 총 {len(review_btn)} 페이지")
            else:
                print(f"상품평 총 {len(review_btn)} 페이지")   
            print()

            #collect all the rating, headline, and contents from the reviews
            
            data_page_num = 1
            while True:
                reviews = driver.find_elements(By.CSS_SELECTOR, ".sdp-review__article__list.js_reviewArticleReviewList")
                
                for review in reviews:
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
                if data_page_num > len(review_btn):
                    break

                review_btn = driver.find_element(By.CSS_SELECTOR, ".js_reviewArticlePageBtn[data-page='{data_page_num}']")
                review_btn.click()
                time.sleep(random.uniform(2,3))
                

if __name__ == '__main__':
    main()