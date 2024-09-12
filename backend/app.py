from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_model import get_response
from document_processing import process_document
from auth import verify_2fa
from profanity_filter import filter_profanity

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Chatbot API! Use the API endpoints to submit queries and upload documents."

predefined_answers = {
    "leave policy": "The company's leave policy allows up to 30 days of paid leave annually.",
    "working hours": "Our working hours are from 9 AM to 5 PM, Monday through Friday.",
    "it support": "For IT support, please contact the IT Helpdesk or visit the FAQ page on the internal portal.",
    "company events": "The next company event is scheduled for the 15th of November. Stay tuned for more updates."
}

@app.route('/submit_query', methods=['POST'])
def submit_query():
    data = request.json
    question = data.get('question', '').lower()  # Convert to lowercase for easier matching

    # Search for a predefined answer
    response = predefined_answers.get(question, "I'm sorry, I don't have an answer for that.")

    return jsonify({"response": response})

@app.route('/query', methods=['POST'])
def handle_query():
    try:
        data = request.json
        user_query = data.get('query', '')
        user_email = data.get('email', '')
        otp = data.get('otp', '')

        if not user_query or not user_email or not otp:
            return jsonify({'error': 'Missing required fields'}), 400

        if not verify_2fa(user_email, otp):
            return jsonify({'error': 'Invalid OTP'}), 401

        response = get_response(user_query)
        filtered_response = filter_profanity(response)
        return jsonify({'response': filtered_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_document():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file part'}), 400
        if not file.filename:
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        summary, keywords = process_document(file)
        return jsonify({'summary': summary, 'keywords': keywords})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    return filename.endswith(('.pdf', '.docx', '.txt'))

if __name__ == '__main__':
    app.run(debug=True)