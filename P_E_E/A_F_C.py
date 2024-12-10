import sys
sys.path.append('../6-12-2024')
import time
start_time = time.time()

from scrapers import reddit_scraper,google_search_scrape
from modules import api_calls_module,small_modules
def collect_feedback_of_the_user(company_name):
    
    scraped_responsr=google_search_scrape.google_search(company_name+"reddit reviews")
    reddit_url=[]
    for url in scraped_responsr:
        check_weather_url_is_reddit=small_modules.is_social_media(url,"reddit")
        print(check_weather_url_is_reddit)
        if check_weather_url_is_reddit==True:
            reddit_url.append(url)
        else:
            pass
    title_list=[]
    explained_list=[]
    comment_list=[]
    for i in reddit_url:
        title,explained,comment=reddit_scraper.reddit_scrape_and_explainer(i,company_name)
        
        title_list.append(title)
        explained_list.append(explained)
        comment_list.append(comment)
    return title_list,explained_list,comment_list


print(collect_feedback_of_the_user("100xengineers"))
final_time=time.time()-start_time
print(final_time)