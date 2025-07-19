import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")  # Use latest available model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        job_description = data.get("job_description")

        prompt = f"""
        You are an expert HR interviewer.

        Generate exactly 4 interview questions:
        - 2 general HR questions (like 'Introduce yourself', 'Why should we hire you?')
        - 2 job-specific questions based on the following job description:

        Job Description:
        {job_description}

        Return only the questions in a numbered list format like:
        1. Question one
        2. Question two
        3. Question three
        4. Question four
        """

        response = model.generate_content(prompt)

        questions_text = response.text

        questions = []
        for line in questions_text.strip().split('\n'):
            if line.strip():
                question = line.strip().split('. ', 1)[-1]
                questions.append(question)

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
