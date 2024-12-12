from urllib import response
from phi.agent import Agent
from phi.tools.tavily import TavilyTools
from typing import List
from rich.pretty import pprint
from pydantic import BaseModel, Field
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq

from phi.utils.pprint import pprint_run_response


import json
from exa_py import Exa
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# gorq models 
# llama-3.1-70b-versatile

# llama-3.3-70b-versatile

# llama-3.2-11b-vision-preview
# llama-3.2-90b-vision-preview
# llama-3.3-70b-specdec

user_startup = "100xEngineering"  # Replace with the actual user startup name
user_startup_website = "https://www.100xengineers.com/"  # Replace with the actual user startup

def get_data_folder(user_startup: str) -> str:
    data_folder = f'data_{user_startup}'
    os.makedirs(data_folder, exist_ok=True)
    return data_folder

data_folder = get_data_folder(user_startup)

# ================================================================



class CompetitorList(BaseModel):
    competitor: List[str] = Field(..., description="List of all the competitors of the startup.")
    competitor_website: List[str] = Field(..., description="List of all website of the startup.")

# Initialize the agent with the specified instructions
company_analysis_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    api_key = "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",
    description=f'You are a business analyst analyzing the company - {user_startup} and Explain in detail',
    instructions= [f'Identify and find websites of competitors of {user_startup} using the Traxcn, business intelligence platform. Select only 3 direct competitor.'],
    tools=[TavilyTools(
        api_key="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",
        include_answer=False,
        search_depth='basic',

    )],
    response_model=CompetitorList,
    structured_response=True

)

company_analysis_agent.print_response("")
# Get the structured response from the agent
response = company_analysis_agent.run()

# Parse the response - it should be a dictionary-like object
if isinstance(response.content, str):
    print("Unexpected string response:", response.content)
    raise ValueError("Agent returned string instead of structured data")

# Access the competitor data
competitor_list = response.content
pprint(competitor_list.competitor)
pprint(competitor_list.competitor_website)
print("Competitor Names:", competitor_list.competitor)
print("Competitor Websites:", competitor_list.competitor_website)



# ================================================================


from exa_py import Exa
import os
import requests

# Fix the company list handling
company_names = competitor_list.competitor[:]  # Create a copy of the list
company_websites = competitor_list.competitor_website[:]  # Create a copy of the list

# Add the user startup to the lists
company_names.append(user_startup)
company_websites.append(user_startup_website)

# Create a dictionary of companies and their websites
companies = dict(zip(company_names, company_websites))

print("Companies:", companies)
print("Company Names:", company_names)
print("Company Websites:", company_websites)

save_path = os.path.join(data_folder, 'companies.json')
with open(save_path, 'w') as f:
    json.dump(companies, f)


exa = Exa(api_key=os.getenv('EXA_API_KEY'))
headers = {
    'Authorization': f"Bearer {os.getenv('JINA_API_KEY')}",
    'X-Return-Format': 'screenshot'
}



# Improved error handling for screenshots
for company, website in companies.items():
    try:
        url = 'https://r.jina.ai/' + website
        print(f"Processing screenshot for {company} with URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        save_path = os.path.join(data_folder, f'{company}_ss.png')
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Screenshot saved for {company} at {save_path}")
    except Exception as e:
        print(f"Error processing screenshot for {company}: {str(e)}")

# # Improved error handling for Exa crawl
# for company, website in companies.items():
#     try:
#         print(f"Processing crawl for {company} with URL: {website}")
#         result = exa.get_contents(
#             [website],
#             text=True,
#             subpages=10,
#             subpage_target=["about", "product", "pricing", "Teams", "Individual", 
#                            "docs", "company", "Who We Are", "about", "contact us", 
#                            "resources", "community", "Investor Relations"]
#         )
        
#         # Save crawl results to text file
#         crawl_file_path = os.path.join(data_folder, f'{company}_crawl.txt')
#         with open(crawl_file_path, 'w', encoding='utf-8') as f:
#             f.write(f"Crawl results for {company} ({website}):\n\n")
#             f.write(str(result))
#         print(f"Crawl result saved to {crawl_file_path}")
        
#     except Exception as e:
#         print(f"Error crawling {company}: {str(e)}")

# ================================================================

