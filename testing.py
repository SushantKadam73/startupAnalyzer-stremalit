import scrapers.url_to_llm_friend as url_to_llm_friend
from C_D_M import C_D_M_agent
import time
start_time=time.time()

#scrapes the webiste in qestion and gives out the summary of the website it takes around 70 seconds to screape and prepare website

give_=url_to_llm_friend.url_to_llm_explainer("https://www.100xengineers.com/")
#gives out the customer discovery module report currently it takes around 130 seconds to comple
CDM_REPORT=C_D_M_agent.customer_discovery_module_agent("100xengineers")
#gives out the 
print(time.time()-start_time)
#all of the test are done using 100xengeneers as test