import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("Google in 2007, few people outside of the company took him ")
doc = nlp(text)
# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
    