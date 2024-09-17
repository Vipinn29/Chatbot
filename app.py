from flask import Flask, request, jsonify
from flask import render_template
import requests
import random
import smtplib
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import os
import PyPDF2
from transformers import pipeline
import concurrent.futures

app = Flask(__name__)

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"
user_otps = {}  # To store OTPs


@app.route('/')
def home():
    return render_template('index.html')

def send_otp(email, otp):
    msg = MIMEText(f'Your OTP is: {otp}')
    msg['Subject'] = 'Your 2FA OTP'
    msg['From'] = 'bytebazaar22@gmail.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('bytebazaar22@gmail.com', 'inekhiosoubwlhjc')
        server.send_message(msg)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    # password = data.get('password')

    # if password == "password123":  # Simulate correct password
    otp = random.randint(100000, 999999)
    user_otps[email] = otp
    send_otp(email, otp)
    return jsonify({'success': True})
    # else:
    #     return jsonify({'success': False}), 401

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    otp = data.get('otp')
    
    for email, user_otp in user_otps.items():
        if str(user_otp) == str(otp):
            del user_otps[email]
            return jsonify({'verified': True})
    return jsonify({'verified': False}), 401

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = request.json.get('message')
    user_id = data.get('user_id')  # Get the unique user ID (email)

    print(f"Received: {user_message}, from user: {user_id}")

    # Payload for sending the message to Rasa
    payload = {
        "sender": user_id,  # This identifies the user in Rasa
        "message": user_message
    }

    response = requests.post(RASA_ENDPOINT, json=payload)
    rasa_responses = response.json()
    if rasa_responses:
        bot_reply = rasa_responses[0].get('text', 'Sorry, I did not understand that.')
    else:
        bot_reply = 'Sorry, I did not understand that.'
    return jsonify({'reply': bot_reply})


# Initialize the summarization pipeline
summarizer = pipeline("summarization", model='t5-small')

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Function to summarize the document using transformers
def summarize_text(text, chunk_size=1000, max_workers=6):
    # Split the text into smaller chunks
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Function to summarize a chunk
    def summarize_chunk(chunk):
        input_length = len(chunk.split())
        # Set max_length to be about 60% of input length, but no more than 250
        max_len = min(int(input_length * 0.6), 150)
        summary = summarizer(chunk, max_length=max_len, min_length=25, do_sample=False)
        return summary[0]['summary_text']
    
    # Use ThreadPoolExecutor for parallel summarization
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        chunk_summaries = list(executor.map(summarize_chunk, text_chunks))
    
    # Combine all chunk summaries into a final summary
    combined_summary = ' '.join(chunk_summaries)
    
    return combined_summary

# Route to handle document upload
@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({'error': 'No document uploaded'}), 400

    # Save uploaded file
    file = request.files['document']
    filename = secure_filename(file.filename)
    file_path = os.path.join(os.getcwd(), filename)
    file.save(file_path)

    # Extract text from the document
    text = extract_text_from_pdf(file_path)

    # Summarize the document (using transformers summarizer)
    summary = summarize_text(text)

    # Clean up the file
    os.remove(file_path)

    # Return summarized text as JSON response
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(port=8000)
