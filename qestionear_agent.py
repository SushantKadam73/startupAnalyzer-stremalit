from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
from modules import small_modules

# and uses the Gemini LLM with various tools to answer the question.  The response is returned as plain text.

def qestion_answer_agent(question,url_of_the_comapny):
    company_name=small_modules.extract_website_name(url_of_the_comapny)
    context_file=open("knowlege_base/"+company_name+"/company_website_details.txt", "r").read()
    instructions = f"You are a helpful assistant. Answer the question based on the context provided. If the context does not contain the answer, search the answer.if you can't find answer,say 'I don't know.'. Do not make up an answer.use context :"+context_file
    if isinstance(instructions, list):
        pass
    else:
        instructions=[instructions]
    m_agent=Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        description="",
        markdown=True,instructions=instructions,
        structured_outputs=True,
        tools=[GoogleSearch()],
        show_tool_calls=True,
        debug_mode=True,
        )
    response = m_agent.run(question)
    return response.content
answer=qestion_answer_agent("find usp of the company","https://www.100xengineers.com/")
print(answer)