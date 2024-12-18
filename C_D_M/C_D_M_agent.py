from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
import sys
sys.path.append('../6-12-2024')
from modules import small_modules
from C_D_M import CJS 
from C_D_M import ICP_generator
from C_D_M import NMA
from C_D_M import VPA
import report_builder
def customer_discovery_module_agent(company_name):
    topic_name="Customer_discovery_module"
    location_of_report="knowlege_base/"+company_name+"/"+topic_name+"_report.md"
    icp,product=ICP_generator.generatr_ICP_refine(company_name)
    need=NMA.need_of_the_customer(product,icp)
    validation=VPA.vpa(product,icp,need)
    customer_journey_simulation=CJS.customer_journey_simulation(company_name)
    print("simulated_journey")
    response=report_builder.report_builder([icp,need,validation,customer_journey_simulation],"Customer_discovery_module",company_name)
    print("build report")
    return response