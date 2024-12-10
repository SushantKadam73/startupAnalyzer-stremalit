from modules import api_calls_module
def expand_to_international_markets(product):
    questions="Competitor offering analysis. what are Market gap relative to the product. how to optimise Product positioning . what are Strategic advantage for my product"
    response=api_calls_module.ask_llm(questions,False,instructions=["use this product as product reference"+product])
    return response
