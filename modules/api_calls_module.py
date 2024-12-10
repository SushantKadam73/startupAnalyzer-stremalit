from phi.agent import Agent
from phi.model.google import Gemini
import requests
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import time
load_dotenv(Path("keys.env"))
print(os.getenv("CONNSTRING"))
jina_api_key=os.getenv("JINA_AI_KEY")
def ask_llm(llm_qes,line_allowed,instructions):
    if isinstance(instructions, list):
        pass
    else:
        instructions=[instructions]
        print("insrtuctions not provided as list exception triggered")

    m_agent=Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        markdown=True,instructions=instructions
        ,structured_outputs=True,
        )
    try:
        response = m_agent.run(str(llm_qes))
        response=response.content
    except:
        time.sleep(60)
        response = m_agent.run(str(llm_qes))
        response=response.content
    fin_response=[]
    tmp=""
    if line_allowed==True:
        for i in response:
            tmp+=i
            if i=="\n":
                fin_response.append(tmp)
                tmp=""
        fin_response = list(set(fin_response))
        try:
            fin_response.remove("\n")
        except:
            pass
        return fin_response
    else:
        return response

def ask_jina(querry):
    url = 'https://s.jina.ai/'+querry
    headers = {
    'Authorization':jina_api_key,
    'X-Retain-Images': 'none',
    'X-With-Links-Summary': 'true','X-Return-Format': 'text'
    }
    response = requests.get(url, headers=headers)
    return (response.text)


def scrape_with_jina(website_url):
    headers = {
        "Accept": "text/event-stream",
        "Authorization": jina_api_key,
        "Content-Type": "application/json",
        "X-With-Generated-Alt": "true",
        "X-With-Links-Summary": "true"
    }

    data = {
    "url": website_url,
    "injectPageScript": [
        "// Remove headers, footers, navigation elements\ndocument.querySelectorAll('header, footer, nav').forEach(el => el.remove());\n\n// Or a url that returns a valid JavaScript code snippet\n// https://example.com/script.js"
        ]
    }

    response = requests.post("https://r.jina.ai/", headers=headers, json=data)
    return response.text

