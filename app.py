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

        <style>

        body {{

            font-family: Arial, sans-serif;
            background-color: #f4f4f4;

            padding: 30px;
        }}

        .container {{

            background: white;

            padding: 30px;

            border-radius: 15px;

            box-shadow: 0px 0px 15px rgba(0,0,0,0.2);

            max-width: 800px;

            margin: auto;
        }}

        .score {{

            color: green;

            font-size: 28px;

            font-weight: bold;
        }}

        .skills {{

            color: blue;
        }}

        .missing {{

            color: red;
        }}

        pre {{

            background: #eee;

            padding: 15px;

            border-radius: 10px;

            white-space: pre-wrap;
        }}

        </style>

        </head>

        <body>

        <div class="container">

        <h1>Resume Analysis Result</h1>

        <h2 class="score">ATS Score: {score}/100</h2>

        <h2 class="skills">Detected Skills:</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in found_skills)}
        </ul>

        <h2 class="missing">Missing Skills:</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in missing_skills)}
        </ul>
        <h2>Suggestions:</h2>

        <ul>
            {''.join(f'<li>{tip}</li>' for tip in suggestions)}
        </ul>
        
        <h2>Extracted Resume Text:</h2>

        <pre>{text}</pre>

        </div>

        </body>

        </html>
        """

    return "No file uploaded"


if __name__ == '__main__':
    app.run(debug=True)