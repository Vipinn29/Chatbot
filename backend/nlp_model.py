from transformers import pipeline

nlp = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

def get_response(query):
    context = "Insert your context or load dynamically from a database"
    result = nlp(question=query, context=context)
    return result['answer']
