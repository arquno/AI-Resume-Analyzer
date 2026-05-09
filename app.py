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

        score = len(found_skills) * 10

        if score > 100:
            score = 100

        return f"""
        <h1>Resume Analysis Result</h1>

        <h2>ATS Score: {score}/100</h2>

        <h2>Detected Skills:</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in found_skills)}
        </ul>

        <h2>Missing Skills:</h2>

        <ul>
            {''.join(f'<li>{skill}</li>' for skill in missing_skills)}
        </ul>

        <h2>Extracted Resume Text:</h2>

        <pre>{text}</pre>
        """

    return "No file uploaded"


if __name__ == '__main__':
    app.run(debug=True)