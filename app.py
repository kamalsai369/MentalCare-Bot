import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure API key is loaded
if not API_KEY:
    raise ValueError("API Key is missing. Please check your .env file.")

# Configure Google AI API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Use "gemini-1.5-pro" if needed

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = model.generate_content(user_message)
        bot_response = response.text.strip() if hasattr(response, "text") else "I'm here to support you!"
    except Exception as e:
        bot_response = "Sorry, I couldn't process your request at the moment."

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
