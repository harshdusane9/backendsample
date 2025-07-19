from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

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

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )

        questions_text = response.text

        # Split questions into list (splitting by newline or numbering)
        questions = []
        for line in questions_text.strip().split('\n'):
            if line.strip():
                # Remove numbering like '1. ', '2. ' etc.
                question = line.strip().split('. ', 1)[-1]
                questions.append(question)

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
