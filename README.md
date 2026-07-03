# Personality Prediction System

A Flask web app that predicts personality traits (Big Five: Openness, Neuroticism,
Conscientiousness, Agreeableness, Extraversion) based on user-provided trait scores,
and extracts basic info (Email, Phone, Skills) from an uploaded resume (PDF/DOCX).

## Features
- Input trait scores (1-10) for the Big Five personality traits
- Get a human-readable personality label for each trait
- Upload a resume (PDF or DOCX) to auto-extract Email, Phone, and Skills
- Simple, responsive web UI

## Tech Stack
- Python, Flask
- PyPDF2 (PDF parsing)
- docx2txt (DOCX parsing)
- HTML, CSS

## Project Structure
```
personality-prediction-system/
├── app.py
├── requirements.txt
├── training_dataset.csv
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Setup & Run

1. Clone the repo
   ```bash
   git clone https://github.com/<your-username>/personality-prediction-system.git
   cd personality-prediction-system
   ```

2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app
   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000/` in your browser.

## Future Improvements
- Train an actual ML model on `training_dataset.csv` instead of static word-mapping
- Improve resume parsing (regex-based email/phone extraction)
- Add input validation and error handling on the frontend

## Author
Ayush
