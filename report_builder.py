from modules import api_calls_module,small_modules
import pypdf
from fpdf import FPDF
import os
def report_builder(datapoint_list,topic_name,company_name):
    location_of_report="knowlege_base/"+company_name+"/"+topic_name+"_report.txt"
    updated_recent,processed_report=small_modules.is_file_present_updated(location_of_report)
    if updated_recent==True:
        return processed_report
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
    return processed_report

def final_report_builder(company_name):
    location_of_report="knowlege_base/"+company_name+"/"+company_name+"_final_report.txt"
    updated_recent,processed_report=small_modules.is_file_present_updated(location_of_report)
    if updated_recent==True:
        return processed_report
    else:
        pass
    report_details=""
    report_list = os.listdir("knowlege_base/"+company_name)
    for reports in report_list:
        if reports.endswith("_report.txt"):
            for details in open("knowlege_base/"+company_name+"/"+reports,"r").readlines():
                report_details+=details
    report_save=open(location_of_report,"w")
    processed_report="".join(report_details)
    report_save.write(processed_report)
    report_save.close()
    return location_of_report
