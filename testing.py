import modules.small_modules
import scrapers.url_to_llm_friend as url_to_llm_friend
from C_D_M import C_D_M_agent
from P_E_E import A_F_C
import time
start_time=time.time()
url="https://www.100xengineers.com"
company_name=modules.small_modules.extract_website_name(url)
give_=url_to_llm_friend.url_to_llm_explainer(url)
#knlogebase/<name_of_the_company>/<name of the report>_report.md
CDM_REPORT=C_D_M_agent.customer_discovery_module_agent(company_name)
AFC_REPORT=A_F_C.collect_feedback_of_the_user(company_name)
#all of the test are done using 100xengeneers as test