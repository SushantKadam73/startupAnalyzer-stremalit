from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
import ICP_generator


class ICP_gen(Toolkit):
    def __init__(self):
        self.company_name=""
        super().__init__(name="icp_generation_tool")
        
        self.register(self.gen_icp)


    def gen_icp(self, company_name: str) -> str:
        """Runs a bot that uses the name of a company to generate an ICP (Individualized Care Plan) for that company. The ICP is a document that outlines the specific care and support that a company needs to improve its performance and achieve its goals. The bot uses a combination of natural language processing, machine learning, and expert knowledge to generate the ICP. The bot also provides recommendations for specific actions that the company can take to improve its performance. 
        The output of the bot are Demographics ,Professional_Profile ,Psychology ,values,behaviours ,media consumption , occupation industry ,challenges ,motivation ,goals.
        and the product

        Args:
            company name  (str): The name of the company that already exist.
        Returns:
            str: the ideal customer profile and the product from which it generated icp.
        """
        import subprocess

        logger.info(f"Running icp on data of the company: {company_name}")
        try:
            
            result = ICP_generator.generatr_ICP_refine(company_name)
            logger.debug(f"Result: {result}")
            # return only the last n lines of the output
            return result
        except Exception as e:
            logger.warning(f"Failed to run: {e}")
            return f"Error: {e}"+"no data avaialable of the company"
        

class ICP_gen(Toolkit):
    def __init__(self):
        
        super().__init__(name="shell_tools")
        self.register(self.gen_icp)

    def gen_icp(self, company_name: str) -> str:
        """Runs a bot that uses the name of a company to generate an ICP (Individualized Care Plan) for that company. The ICP is a document that outlines the specific care and support that a company needs to improve its performance and achieve its goals. The bot uses a combination of natural language processing, machine learning, and expert knowledge to generate the ICP. The bot also provides recommendations for specific actions that the company can take to improve its performance. 
        The output of the bot are Demographics ,Professional_Profile ,Psychology ,values,behaviours ,media consumption , occupation industry ,challenges ,motivation ,goals.
        and the product

        Args:
            company name  (str): The name of the company that already exist.
        Returns:
            str: the ideal customer profile and the product from which it generated icp.
        """
        import subprocess

        logger.info(f"Running icp on data of the company: {company_name}")
        try:
            
            result = ICP_generator.generatr_ICP_refine(company_name)
            logger.debug(f"Result: {result}")
            # return only the last n lines of the output
            return result
        except Exception as e:
            logger.warning(f"Failed to run: {e}")
            return f"Error: {e}"+"no data avaialable of the company"