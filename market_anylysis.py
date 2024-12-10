from modules import api_calls_module
def expand_to_international_markets(product):
    questions="what are Real-time market trend for the product.who are my competitiors. what are oppurtunities available"
    response=api_calls_module.ask_llm(questions,False,instructions=["use this product as product reference"+product])
    return response
