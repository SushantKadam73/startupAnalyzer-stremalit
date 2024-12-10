from phi.agent import Agent
from phi.model.google import Gemini
from phi.storage.agent.sqlite import SqlAgentStorage
import time
def taklking(talk,id_of_the_char,character_descirption,output_format_list,special_inst):
    if isinstance(talk, list):
        pass
    else:
        talk=[talk]
    
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        instructions=[character_descirption,"stick by this persona i have given i gave you","talk and act like persona i gave you","think like person i gave you",special_inst],
        storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
        add_history_to_messages=True,
        num_history_responses=100,
        session_id=id_of_the_char,)
    response_list=[]
 
    for sentences in talk:
        try:
            response=agent.run(sentences)
            response_list.append(response.content)
        except:
            time.sleep(60)
            response=agent.run(sentences)
            response_list.append(response.content)
    if output_format_list==True:
        return response_list
    else:
        return " ".join(response_list)


