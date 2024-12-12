from modules import api_calls_module as api_call_pro
import re
from modules import small_modules
import os
import time

def url_to_llm_explainer(url):
    usable_website_data=""
    important_urls=[]
    spare_urls=[]
    main_points=""
    name_of_file=small_modules.extract_website_name(url)
    isExist = os.path.exists("knowlege_base/"+name_of_file)
    if not isExist:
        os.makedirs("knowlege_base/"+name_of_file)
    else:
        last_updated_time=os.path.getmtime("knowlege_base/"+name_of_file+"/company_website_details.txt")
        if last_updated_time+86400<time.time():
            pass
        else:
            for i in open("knowlege_base/"+name_of_file+"/company_website_details.txt","r"):
                usable_website_data+=i
            for i in open("knowlege_base/"+name_of_file+"/important_urls.txt","r"):
                important_urls.append(i.strip())
            for i in open("knowlege_base/"+name_of_file+"/spare_urls.txt","r"):
                spare_urls.append(i.strip())
            for i in open("knowlege_base/"+name_of_file+"/main_points.txt","r"):
                main_points+=i
            return [usable_website_data,important_urls,spare_urls,main_points]
    promblems_in_scraping=True
    while promblems_in_scraping!=False:    
        tmp=api_call_pro.scrape_with_jina(url)
        if tmp.startswith("event: error"):
            pass

        else:
            promblems_in_scraping=False
            usable_website_data=api_call_pro.ask_llm(tmp,False,["convert the given data into human readable way",
            "Company Profile, About, Coverage Areas, People, founders and their socials,",
            "Cap Tables, Investments & Acquisitions Exits, Funding & Investors",
            "Competitive Landscape, Competitors, Explore Similar, Comparable",
            "Market share and retention, Reports, News",
            "Financials, Key Metrics, Metrics",
            "Social Media profile and metrics"
            ])



        
    url_store=""
    url_array=[]
    url_register_available=False

    for i in tmp:
        if i=="(":
            url_register_available=True

        elif i==")":
            url_register_available=False
            url_array.append(url_store)
            url_store=""

        elif url_register_available==True:
            url_store+=i

    spare_urls=[]
    important_urls=[]
    for i in url_array:
        reconsider_visiting=False

        subdomain_counter=0
        for j in i:
            if j=="/":
                subdomain_counter+=1
            if subdomain_counter>3:
                reconsider_visiting=True
                break
        if reconsider_visiting==True :
            spare_urls.append(i)
        else:
            important_urls.append(i)
    important_urls= list(set(important_urls))
    spare_urls= list(set(spare_urls))
    main_points=api_call_pro.ask_llm(tmp,False,"what are the main points in this data")
    save_data=open("knowlege_base/"+name_of_file+"/company_website_details.txt","w",encoding="utf-8")
    save_data.write(usable_website_data)
    save_data.close()
    save_data=open("knowlege_base/"+name_of_file+"/important_urls.txt","w",encoding="utf-8")
    for i in important_urls:
        save_data.write(i+"\n")
    save_data.close()
    save_data=open("knowlege_base/"+name_of_file+"/spare_urls.txt","w",encoding="utf-8")
    for i in spare_urls:
        save_data.write(i+"\n")
    save_data.close()
    save_data=open("knowlege_base/"+name_of_file+"/main_points.txt","w",encoding="utf-8")
    save_data.write(main_points)
    save_data.close()
    save_data=open("knowlege_base/"+name_of_file+"/raw_data.txt","w",encoding="utf-8")
    save_data.write(tmp)
    save_data.close()
    context_file=open("knowlege_base/"+name_of_file+"/company_website_details.txt", "r").read()
    context=api_call_pro.ask_llm(context_file,False,["what is the product in following .please provide a detailed description","only include details that are present in the following"])
    open("knowlege_base/"+name_of_file+"/product.txt", "w").write(context)
    
    return [usable_website_data,important_urls,spare_urls,main_points]