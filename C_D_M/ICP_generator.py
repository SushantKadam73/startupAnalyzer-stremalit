import sys
sys.path.append('../6-12-2024')
from modules import api_calls_module,small_modules
def generatr_ICP(company_name):
    context_file=open("knowlege_base/"+company_name+"/product.txt", "r").read()
    context=api_calls_module.ask_llm(context_file,False,["what is the product in following .please provide a detailed description","only include details that are present in the following"])
    response=api_calls_module.ask_llm(context,True,["according to product what are the target customer's Demographics ,Professional_Profile ,Psychology ,values,behaviours ,media consumption , occupation industry ,challenges ,motivation  ,goals","give me answer 10 words each"])
    
    return [response,context]

def file_ICP(icp_data,product):
    response=api_calls_module.ask_llm(icp_data,False,["are Demographics ,Professional_Profile ,Psychology ,values,behaviours ,media consumption , occupation industry ,challenges ,motivation ,goals are correct for the product"
                                                     ,"if yes then start_with 'YES' else give me"
                                                     ,"do not add explaination and only give the specific"
                                                     ,"your product to judge is here:"+product])
    return response

def generatr_ICP_refine(company_name):
    
    icp_verified=False
    response="NO Run"
    product=""
    response=""
    while icp_verified==False:
        
        if response.startswith("YES"):
            response=response.lower()
            response=response.replace("YES","")
            icp_verified=True
            response=icp
        else:
            context_file=open("knowlege_base/"+company_name+"/company_website_details.txt", "r").read()
            context=api_calls_module.ask_llm(context_file,False,["what is the product in following .please provide a detailed description","only include details that are present in the following"])
            open("knowlege_base/"+company_name+"/product.txt", "w").write(context)
            icp_data=generatr_ICP(company_name)
            icp="".join(icp_data[0])
            print(icp_data[0])
            product=icp_data[1]
            response=file_ICP(icp,product)
    open("knowlege_base/"+company_name+"/icp.txt", "w").write(response)
    return response,product

