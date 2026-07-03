from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import docx2txt

app = Flask(__name__)

# ---------- Trait Words ----------
TRAIT_WORDS = {
    "Openness": ["Reserved", "Cautious", "Practical", "Curious", "Imaginative",
                 "Creative", "Inventive", "Insightful", "Visionary", "Genius"],
    "Neuroticism": ["Calm", "Relaxed", "Stable", "Balanced", "Sensitive",
                    "Emotional", "Moody", "Tense", "Anxious", "Highly Sensitive"],
    "Conscientiousness": ["Careless", "Occasionally Careless", "Somewhat Reliable", "Moderate",
                          "Responsible", "Organized", "Dependable", "Very Responsible",
                          "Highly Dependable", "Perfectionist"],
    "Agreeableness": ["Aloof", "Reserved", "Neutral", "Somewhat Friendly", "Cooperative",
                      "Friendly", "Warm", "Very Friendly", "Compassionate", "Highly Cooperative"],
    "Extraversion": ["Shy", "Reserved", "Quiet", "Calm", "Sociable",
                     "Outgoing", "Energetic", "Very Energetic", "Extroverted", "Highly Outgoing"]
}


# ---------- Helper Functions ----------
def extract_resume_data(file):
    """Extract Email, Phone, Skills from uploaded resume (PDF or DOCX)"""
    try:
        extension = file.filename.split('.')[-1].lower()
        text = ""
        if extension == "pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        elif extension in ["doc", "docx"]:
            text = docx2txt.process(file)
        else:
            return {}

        info = {}
        for line in text.splitlines():
            line_lower = line.lower()
            if "@" in line_lower and "Email" not in info:
                info["Email"] = line.strip()
            elif any(c.isdigit() for c in line_lower) and "Phone" not in info:
                info["Phone"] = line.strip()
            elif "skill" in line_lower and "Skills" not in info:
                info["Skills"] = line.strip()
        return info
    except Exception as e:
        print("Resume extraction error:", e)
        return {}


def map_to_words(inputs):
    """Map trait scores 1-10 to words"""
    result = {}
    traits = ["Openness", "Neuroticism", "Conscientiousness", "Agreeableness", "Extraversion"]
    for i, trait in enumerate(traits):
        try:
            val = int(inputs[i])
            val = max(1, min(10, val))  # Ensure 1-10
            result[trait] = TRAIT_WORDS[trait][val - 1]
        except Exception as e:
            result[trait] = "Unknown"
    return result


# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    resume_info = {}
    if request.method == "POST":
        try:
            # Get trait scores from form
            inputs = [
                request.form.get("openness", 1),
                request.form.get("neuroticism", 1),
                request.form.get("conscientiousness", 1),
                request.form.get("agreeableness", 1),
                request.form.get("extraversion", 1)
            ]
            result = map_to_words(inputs)

            # Extract resume info if uploaded
            resume_file = request.files.get("resume")
            if resume_file and resume_file.filename != "":
                resume_info = extract_resume_data(resume_file)

        except Exception as e:
            result = {"Error": str(e)}

    return render_template("index.html", result=result, resume_info=resume_info)


if __name__ == "__main__":
    app.run(debug=True)
