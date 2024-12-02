from phi.agent import Agent
from phi.model.google import Gemini
from phi.agent import Agent, RunResponse
from typing import Iterator
from pydantic import BaseModel, Field
import json
def ideal_customer_profile(product_description):
    icp_agent=Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        markdown=True,instructions=["suggent the ideal customers for the given description of the product",
                                    "the ideal customer profile must only include these Demographics ,Professional_Profile ,Psychology ,values,behaviours ,media consumption , occupation industry ,challenges ,motivation  ,goals",
                                    "answer in 10 words each",
                                    "make sure the information is correct",
                                    "give pricise labels that leaves no confusion",
                                    "give relatively favorable Ideal Customer Profile",
                                    "provide in format that is like ='description':{....,....}'"
                                    ]
        ,structured_outputs=True,
    )
    response = icp_agent.run(str(product_description))
    response=response.content

    return response
def create_profile(personas_details):
    icp_agent=Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        markdown=True,instructions=["give me in the format of single line descriptions of each character"]
        )
    response =icp_agent.run(str("create 20 persons on this data :"+personas_details))
    response=response.content
    fin_response=[]
    tmp=""
    for i in response:
        tmp+=i
        if i=="\n":
            fin_response.append(tmp)
            tmp=""
    return fin_response
def qestions_for_personas(qestions,persona,description):
    response=[]
    if isinstance(qestions, list):
        pass
    else:
        print("qestions must be list")
        return None
    for i in qestions:
        persona_agent="you are "+persona+" and you are answering the questions"
        product="the description product your opinion will be asked for is"+description
        icp_agent=Agent(
            model=Gemini(id="gemini-1.5-flash-8b"),
            markdown=True,instructions=[persona_agent]

            ,structured_outputs=True,
        )
        tmp = icp_agent.run(str(i))
        response.append(tmp.content)
    return response

