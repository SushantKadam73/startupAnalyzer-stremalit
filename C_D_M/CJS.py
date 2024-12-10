import sys
sys.path.append('../6-12-2024')
from modules import api_calls_module,talking_agent,small_modules
import csv
def customer_jorney_setup(product,company_name):
    response=api_calls_module.ask_llm("what are the steps a customer will go through while using the product",False,["do not make up answer","give answer according to only the product and product_phases","product :"+str(product)])
    open("knowlege_base/"+company_name+"/product_phases.txt","w").write(str(response))
    return response

def generate_retrive_personas(comapany_name):
    file_is="knowlege_base/"+comapany_name+"/personas.csv"
    file_check,content=small_modules.is_file_present_updated(file_is)
    fileds=[]
    rows=[]
    if file_check==True:
        with open(file_is, 'r') as csvfile:
            list_read_csv = csv.reader(csvfile)
            fileds=next(list_read_csv)
            for read_row in list_read_csv:
                print(read_row)
                rows.append(read_row)
        
    else:
        id_last_used=0
        with open("knowlege_base/globals_store.csv", 'r') as csvfile:
            list_read_csv = csv.reader(csvfile)
            for read_row in list_read_csv:
                id_last_used=read_row[0]
        icp=open("knowlege_base/"+comapany_name+"/icp.txt","r").read()
        response=api_calls_module.ask_llm(icp,True,["generate 10 personas depending on icp","you can use upto 60 word for a line","give me only the persona description and in one line each"])
        with open(file_is, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["persona_id", "persona_description"])
            count=0
            for i in range(int(id_last_used)+1,int(id_last_used)+11):
                count+=1
                rows.append([i,response[count-1]])
                writer.writerow([i,response[count-1]])
        open("knowlege_base/globals_store.csv","w").write(str(id_last_used+10))

    persona_ids=[]
    persona_ids_description=[]
    count=0
    
    for i in rows:
        persona_ids.append(i[fileds.index("persona_id")])
        persona_ids_description.append(i[fileds.index("persona_description")]) 
        count+=1
    return  persona_ids,persona_ids_description
        
def customer_journey_simulation(company_name):
    product=open("knowlege_base/"+company_name+"/product.txt","r").read
    #how can we use this product what are the steps a customer will go through
    product_phases=customer_jorney_setup(product,company_name)
    #generate personas depending on icp
    persona_ids,persona_ids_description=generate_retrive_personas(company_name)
    questions_for_persona=["how was their expereince","if they would recommend the product to others","if they have any suggestions for improvement","if they have any questions about the product","if they loved the product or it is purchasable for them"]
    all_persona_responses=[]
    questions_for_persona=" ".join(questions_for_persona)
    questions_for_persona="answer these question as you have walked through my product:"+questions_for_persona
    print(questions_for_persona)
    for i in range(1,11):
        #let persona walkthrough the steps
        persona_response=talking_agent.taklking(questions_for_persona,str(persona_ids[i-1]),str("you are "+persona_ids_description[i-1]),False,"you have experincinced the produc in this way :"+product_phases)
        all_persona_responses.append(str(i)+":"+persona_response)
    file_save=open("knowlege_base/"+company_name+"/persona_responses.txt","w").write("\n".join(all_persona_responses))
    return all_persona_responses