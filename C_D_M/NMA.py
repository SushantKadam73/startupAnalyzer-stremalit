#Algorithms that help map customer needs and preferences, often used in service design and smart city planning.

from modules import api_calls_module,talking_agent,small_modules
def need_of_the_customer(product,icp):
    response=api_calls_module.ask_llm("What are the common needs and preferences of the customers who are interested in "+product+" and belong to the "+icp+"?",False,["answer the qeuestion according to the product only"])
    return response
