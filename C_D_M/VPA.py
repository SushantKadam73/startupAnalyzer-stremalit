#Automating the validation process to ensure that customer needs and solutions are accurately identified and validated.
from modules import api_calls_module,talking_agent,small_modules
def vpa(product,icp,need):
    response=api_calls_module.ask_llm("does the need matches to the product and how it matches ",False,["answer the qeuestion according to the product only","needs are :"+need,"product is :"+product,"ideal customer profile is is :"+icp])
    return response
