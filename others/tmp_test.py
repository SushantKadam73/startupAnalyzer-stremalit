from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
from phi.vectordb.chroma import ChromaDb

from phi.knowledge.document import DocumentKnowledgeBase
from modules import small_modules
company_name="knowlege_base/100xengineers"
knowledge_base = DocumentKnowledgeBase(
            path=[company_name],
            vector_db=ChromaDb(collection="companies_kb_vdb"),)
# This section defines a function that answers questions about a company using a large language model (LLM),
# a knowledge base, and Google Search.  It extracts the company name from a URL, sets instructions for the LLM, 
# and uses the Gemini LLM with various tools to answer the question.  The response is returned as plain text.

def qestion_answer_agent(question,url_of_the_comapny):
    company_name=small_modules.extract_website_name(url_of_the_comapny)

    instructions = f"You are a helpful assistant. Answer the question based on the context provided. If the knowlegebase does not contain the answer, search the answer.if you can't find answer,say 'I don't know.'. Do not make up an answer.use knowlege base."
    if isinstance(instructions, list):
        pass
    else:
        instructions=[instructions]
    m_agent=Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        description="",
        markdown=True,instructions=instructions,
        structured_outputs=True,
        tools=[GoogleSearch(),],
        show_tool_calls=True,
        debug_mode=True,
        knowledge_base = knowledge_base
        )
    response = m_agent.run(question)
    return response.content
qestion_answer_agent("what is the mission of the company?","https://www.100xengineers.com/")
