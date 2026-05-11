from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['resume']

    if file:

        pdf_reader = PyPDF2.PdfReader(file)

        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        # Skills list
        skills = [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "React",
            "Node.js",
            "SQL",
            "Flask",
            "AWS",
            "Azure",
            "Machine Learning",
            "HTML",
            "CSS"
        ]

        found_skills = []

        # Check skills in resume
        for skill in skills:

            if skill.lower() in text.lower():
                found_skills.append(skill)

        # ATS Score Calculation
        # Required skills for target job
        required_skills = [
            "Python",
            "SQL",
            "Flask",
            "AWS",
            "Machine Learning"
        ]

        missing_skills = []

        for skill in required_skills:
            if skill not in found_skills:
                missing_skills.append(skill)
        # Suggestions for missing skills

        suggestions = []

        for skill in missing_skills:

            if skill == "Flask":
                suggestions.append("Learn Flask for backend development.")

            elif skill == "AWS":
                suggestions.append("Build cloud projects using AWS.")

            elif skill == "SQL":
                suggestions.append("Practice database queries using SQL.")

            elif skill == "Machine Learning":
                suggestions.append("Work on ML projects using Python.")

            elif skill == "Python":
                suggestions.append("Strengthen Python programming fundamentals.")

        score = len(found_skills) * 10

        if score > 100:
            score = 100

        return f"""

        <html>

        <head>

        <title>AI Resume Analyzer</title>

        <style>

        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            padding: 40px;
        }}

        .container {{

            max-width: 900px;
            margin: auto;

            background: rgba(255,255,255,0.08);

            border-radius: 20px;

            padding: 40px;

            box-shadow: 0px 0px 30px rgba(0,0,0,0.5);
        }}

        .score {{

            font-size: 60px;

            font-weight: bold;

            color: {'#22c55e' if score >= 70 else '#facc15' if score >= 40 else '#ef4444'};
        }}

        .progress-container {{

        width: 100%;

        height: 30px;

        background: rgba(255,255,255,0.2);

        border-radius: 20px;

        margin-top: 20px;

        overflow: hidden;
    }}

    .progress-bar {{

        height: 100%;

        border-radius: 20px;

        background: linear-gradient(90deg, #22c55e, #4ade80);

        animation: fillBar 2s ease;
    }}

        @keyframes fillBar {{

            from {{
                width: 0%;
            }}

            to {{
                width: 100%;
            }}
        }}

        .section {{

            margin-top: 30px;

            padding: 25px;

            border-radius: 15px;

            background: rgba(255,255,255,0.08);
        }}

        h1 {{
            text-align: center;
        }}

        ul {{
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 10px;
        }}

        pre {{
            white-space: pre-wrap;

            background: rgba(0,0,0,0.3);

            padding: 20px;

            border-radius: 10px;
        }}

        </style>

        </head>

        <body>

        <div class="container">

        <h1>🚀 AI Resume Analyzer</h1>

        <div class="section">

        <h2>ATS SCORE</h2>

        <div class="score">{score}/100</div>

        <div class="progress-container">

            <div class="progress-bar" style="width:{score}%;">
            </div>

        </div>

        <h3>
        {
            "🟢 Excellent Resume!" if score >= 80 else
            "🟡 Good Resume But Needs Improvement!" if score >= 50 else
            "🔴 Weak Resume - Improve Skills!"
        }
        </h3>

        </div>

        <div class="section">

        <h2>✅ Detected Skills</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in found_skills)}
        </ul>

        </div>

        <div class="section">

        <h2>❌ Missing Skills</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in missing_skills)}
        </ul>

        </div>

        <div class="section">

        <h2>💡 Suggestions</h2>

        <ul>
            {''.join(f'<li>{tip}</li>' for tip in suggestions)}
        </ul>

        </div>

        <div class="section">

        <h2>📄 Extracted Resume Text</h2>

        <pre>{text}</pre>

        </div>

        </div>

        </body>

        </html>

        """
    return "No file uploaded"


if __name__ == '__main__':
    app.run(debug=True)