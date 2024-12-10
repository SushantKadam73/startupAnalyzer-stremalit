from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
import sys
sys.path.append('../6-12-2024')
from C_D_M import CJS 
from C_D_M import ICP_generator
from C_D_M import NMA
from C_D_M import VPA
import report_builder
def customer_discovery_module_agent(company_name):
    icp,product=ICP_generator.generatr_ICP_refine(company_name)
    need=NMA.need_of_the_customer(product,icp)
    validation=VPA.vpa(product,icp,need)
    customer_journey_simulation=CJS.customer_journey_simulation(company_name)
    response=report_builder.report_builder([icp,need,validation,customer_journey_simulation],"Customer discovery module",company_name)
    return response