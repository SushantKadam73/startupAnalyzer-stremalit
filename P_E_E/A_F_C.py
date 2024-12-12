import sys
sys.path.append('../6-12-2024')
import time
start_time = time.time()

from scrapers import reddit_scraper,google_search_scrape
from modules import api_calls_module,small_modules
import report_builder
def collect_feedback_of_the_user(company_name):
    product=open("knowlege_base/"+company_name+"/product.txt", "r").read()

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
    explained_data_to_llm=""
    for i in reddit_url:
        try:
            title,explained,comment=reddit_scraper.reddit_scrape_and_explainer(i,company_name)
            title_list.append(title)
            explained_list.append(explained)
            comment_list.append(comment)
            explained_data_to_llm+="".join(str("post:"+title+"\n \n comments:\n"+explained))

        except:
            pass
    response=api_calls_module.ask_llm("according to this data about the product tell me how is the sentiment data:",False,["do not make up answers use and quote what is the data while explaination.","product:"+str(product)])
    response=report_builder.report_builder([response],"product evalution engine",company_name)
