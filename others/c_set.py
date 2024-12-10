import chromadb.utils.embedding_functions as embedding_functions
# use directly
google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="YOUR_API_KEY")
google_ef(["knowlege_base\100xengineers\company_website_details.txt","knowlege_base\100xengineers\important_urls.txt","knowlege_base\100xengineers\main_points.txt","knowlege_base\100xengineers\raw_dat.txt","knowlege_base\100xengineers\spare_urls.txt"])
# pass documents to query for .add and .query
collection = client.create_collection(name="name", embedding_function=google_ef)