# Chatbot Project with Rasa

## Project Overview
This project is a chatbot built using the Rasa framework. It includes the necessary configurations, training data, and custom actions to create an interactive conversational agent.

## Prerequisites
- Python 3.10.x
- Rasa framework installed in a virtual environment
- Basic knowledge of Rasa and chatbot development

## Setup Instructions

1. **Activate the virtual environment**

On Windows, run the following command to activate the virtual environment:

```bat
C:\Users\DeLL\Chatbot\virtual_env\Scripts\activate.bat
```

2. **Verify Python version**

Ensure you are using Python 3.10.11 as required:

```bat
python --version
```

## Training the Rasa Model

To train the Rasa model with the provided training data and configuration, run:

```bat
rasa train
```

This will generate the model files in the `rasa/models/` directory.

## Running the Chatbot Server

To start the Rasa server with API enabled and CORS allowed, run:

```bat
rasa run --enable-api --cors "*"
```

## Running the Application

To run the main application script, execute:

```bat
python app.py
```

## Project Structure

- `rasa/` - Contains Rasa configuration, domain, data, actions, and endpoints.
- `static/` - Static assets such as images, JavaScript, and CSS files.
- `templates/` - HTML templates for the web interface.
- `virtual_env/` - Python virtual environment directory.
- `app.py` - Main application script to run the chatbot interface.

## Additional Notes

- Make sure to activate the virtual environment before running any commands.
- Update training data in `rasa/data/` to improve chatbot responses.
- Custom actions can be added or modified in `rasa/actions/`.
