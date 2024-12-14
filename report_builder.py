from modules import api_calls_module,small_modules
import pypdf
from fpdf import FPDF
import os
def report_builder(datapoint_list,topic_name,company_name):
    if isinstance(datapoint_list,list):
        pass
    else:
        datapoint_list=[datapoint_list]
    location_of_report="knowlege_base/"+company_name+"/"+topic_name+"_report.md"
    updated_recent,processed_report=small_modules.is_file_present_updated(location_of_report)
    if updated_recent==True:
        return location_of_report
    else:
        pass
    report_data=[]
    for data_point in datapoint_list:
        report_points=api_calls_module.ask_llm(data_point,False,["you are a helpful assistant","you are a helpful assistant that is good at writing reports","you are a helpful assistant that is good at writing reports in a professional and consice yet insightful ways","do not make up and details use the data i am giving you and dont provide explaination just give me report"])
        report_data.append(report_points)
    
    report_save=open(location_of_report,"w")
    processed_report="".join(report_data)
    report_save.write(processed_report)
    report_save.close()
    return location_of_report


def product_analysis(company_name,instructions):
    product=open("knowlege_base/"+company_name+"/product.txt").read()
    response=api_calls_module.ask_llm(product,False,instructions)
    response=report_builder([response],"product_anylysis",company_name)
    return response


def final_report_builder(company_name):
    Reprot_inst="Report Structure: 1. **Introduction** (No Research Needed)      - Provide a brief overview of the startup's industry or topic area.      - Set the context for why a competitor analysis is critical for this startup.      - Define the purpose of the report (e.g., to identify market opportunities, enhance positioning, and improve offerings).   2. **Main Body Sections:**      **A. Competitor Research**      - One dedicated section for EACH competitor in the user-provided list.      - For each competitor, examine:        - **Core Features**:          - A bulleted list of the most notable features of the competitor's products/services.        - **Competitor Offering Analysis**:          - Assess the quality, breadth, and uniqueness of their offerings.        - **Benchmarking Across Key Metrics**:          - Evaluate aspects such as:            - **Quality** (e.g., product/service performance)            - **Pricing** (e.g., affordability vs. perceived value)            - **Customer Satisfaction** (e.g., reviews, testimonials, surveys)            - **Brand Reputation** (e.g., market perception, awards, or recognitions)            - **Financial Health** (e.g., funding, profitability, or stability)        - **Differentiation**:          - Highlight unique aspects of the competitor’s offerings compared to others in the market.        - **Market Positioning**:          - Analyze where the competitor stands in the market:            - Niche player, contender, leader, high performer, etc.      **B. Competitor Analysis Summary**      - Use insights from the competitor research to identify opportunities for the user-provided startup:        - **Competitor Analysis**: Competitor Analysis using one of the seven framework.       - **Market Gap Identification**:          - What unmet needs or underserved segments can the startup target?        - **Product/Service Positioning Optimization**:          - How can the startup differentiate itself or redefine its position in the market?        - **Strategic Advantage Mapping**:          - Identify actionable steps to gain a competitive edge based on competitor weaknesses or gaps. 3. **Conclusion with Comparison Table** (No Research Needed)      - Summarize findings in a structured **comparison table**:        - Columns: Competitor Names (and the user-provided startup).        - Rows: Key comparison dimensions (e.g., quality, pricing, features, reputation).        - Highlight relative strengths and weaknesses for each entity.      - Provide **final recommendations**:        - Actionable insights for improving the startup's offerings, positioning, or strategy based on the analysis."
    instructions=["you are a helpful report agent who takes in data and provide a highly detailes report of mutiple pages","do not make up any extra deatils but you can express the current details fromm the data",]
    product_analysis(company_name,instructions)
    location_of_report="knowlege_base/"+company_name+"/"+company_name+"_final_report.md"
    updated_recent,processed_report=small_modules.is_file_present_updated(location_of_report)
    if updated_recent==True:
        return processed_report
    else:
        pass
    report_details=[]
    report_list = os.listdir("knowlege_base/"+company_name)
    report_save=open(location_of_report,"w")
    for reports in report_list:
        if reports.endswith("_report.md"):
            print(reports)
            details=open("knowlege_base/"+company_name+"/"+reports,"r").read()
            report_details.append(details)
            processed_report="".join(report_details)
    Report_data="the data to make upon the report is :"+str("".join(report_details))
    comb_instructions=instructions+[Reprot_inst]

    response=api_calls_module.ask_llm(Report_data,False,comb_instructions)
    report_save.write("---Overall summary of the report---\n"+response+"\n")
    report_save.write("---Detailed report---\n")
    response=api_calls_module.ask_llm(Report_data,False,["you are a helpful report assisatant","do not make details use only the dtails i provide","write a 20000 word report","write in a simple languge so that a 18 year old could understand"])
    report_save.write(response+"\n")
    report_save.close()
    return location_of_report