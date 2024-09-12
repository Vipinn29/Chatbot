import PyPDF2
from tika import parser
import spacy
from summa import summarizer

nlp = spacy.load("en_core_web_sm")

def process_document(file):
    if file.filename.endswith('.pdf'):
        pdf_text = extract_text_from_pdf(file)
    elif file.filename.endswith('.txt'):
        txt_text = file.read().decode('utf-8')
    else:
        return "Unsupported file type", []

    summary = summarizer.summarize(pdf_text)
    keywords = extract_keywords(pdf_text)
    return summary, keywords

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extract_text()
    return text

def extract_keywords(text):
    doc = nlp(text)
    keywords = [ent.text for ent in doc.ents]
    return keywords
