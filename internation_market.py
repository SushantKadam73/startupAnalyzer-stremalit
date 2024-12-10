from modules import api_calls_module
def expand_to_international_markets(product):
    questions="how to expand the product to international markets. perform International market analysis. find Cultural compatibility assessment .is it Regulatory compliance guidance .Localized growth strategy generation"
    response=api_calls_module.ask_llm(questions,False,instructions=["use this product as product reference"+product])
    return response
