# 🎯 HireLens

> **“See your resume through the eyes of recruiters.”**

HireLens is a production-ready, AI-powered career platform that analyzes resumes against target job descriptions. It calculates weighted ATS compatibility scores, extracts technical and soft skills, performs semantic matching, detects skill gaps, and delivers actionable recruiter-grade optimization recommendations.

---

## 🌟 Key Features

- **📄 Smart Resume Parsing**: Extracts structured text and section blocks (Experience, Education, Projects, Skills, Certifications) from PDF resumes using PyMuPDF (`fitz`).
- **🎯 Weighted ATS Scoring Engine**:
  - **Skill Match**: 35%
  - **Semantic AI Match**: 25%
  - **Keyword Overlap**: 15%
  - **Experience Alignment**: 15%
  - **Education Alignment**: 10%
- **🧠 Semantic AI Matching**: Calculates contextual document similarity between resume achievements and job requirements using TF-IDF n-grams and cosine vectorization.
- **🧩 Categorized Skill Gap Analysis**: Identifies matched skills, missing skills, and additional skills grouped by tech domain (Programming, AI/ML, Cloud, Databases, Frameworks, Tools, Soft Skills).
- **💡 Recruiter-Grade AI Recommendations**: Generates personalized, non-misleading advice to format bullet points, quantify results, and highlight target competencies effectively.
- **💼 Multi-Job Fit Comparison ("Which Job Fits Me Best?")**: Compare a single resume against up to 4 job postings simultaneously to discover your highest matching opportunity.
- **📊 Recruiter Analytics Dashboard**: Interactive Plotly score breakdown gauges, history charts, skill distribution graphs, and summary statistics.
- **📥 Professional Report Exports**: Export detailed analysis reports in HTML (printable to PDF) or clean TXT formats.
- **🎨 Premium AI SaaS Theme**:
  - Toggle between **🌙 Dark Mode** and **☀️ Light Mode**.
  - **Dual-Layer Magnetic Glowing Cursor** & neon click ripple bloom effects.
  - Touchscreen gesture feedback and reduced motion accessibility options.
- **🔐 Secure User Authentication & Persistence**: Password hashing (PBKDF2/SHA256) and SQLite database history storage.

---

## 🛠️ Technology Stack

| Domain | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, Custom HTML5/CSS3, JavaScript |
| **PDF Processing** | PyMuPDF (`fitz`) |
| **NLP & AI** | spaCy, NLTK, Scikit-learn (TF-IDF & Cosine Similarity) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Database** | SQLite3 |
| **Authentication** | PBKDF2 HMAC SHA-256 Hashing |

---

## 🗂️ Project Structure

```
HIRE-LENS/
├── app.py                      # Main entrypoint, navigation router, session state
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
├── .gitignore                  # Git ignore rules
│
├── data/
│   └── skills.json             # Categorized tech & soft skills taxonomy database
│
├── database/
│   └── hirelens.db             # SQLite database (Users & Analysis history)
│
├── utils/
│   ├── theme.py                # Custom CSS/JS styling, Dark/Light modes, Magnetic cursor
│   ├── database.py             # SQLite DAO & user authentication schema
│   ├── authentication.py       # Session management & user signup/login forms
│   ├── pdf_processor.py        # PyMuPDF PDF text & section parsing engine
│   ├── skill_extractor.py      # Regex & word boundary skill extraction
│   ├── semantic_matcher.py     # TF-IDF & Cosine similarity semantic matcher
│   ├── ats_calculator.py       # Multi-factor weighted ATS scoring algorithm
│   ├── resume_analyzer.py      # Main pipeline coordinating extraction & AI recommendations
│   └── report_generator.py    # Report builder for PDF/HTML/TXT exports
│
└── pages/
    ├── home.py                 # Landing page with hero banner & feature cards
    ├── analyzer.py             # PDF Upload, Job Description input, Step analysis, ATS Gauge, Skill breakdown
    ├── dashboard.py            # Recruiter/Candidate Analytics Dashboard with Plotly charts
    ├── jobs.py                 # Multi-job fit comparison ("Which Job Fits Me Best?")
    ├── history.py              # Saved analysis records & report downloads
    ├── profile.py              # Candidate user profile & security settings
    └── settings.py             # Theme toggle (Dark/Light), Reduced Motion, Clear History
```

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/HIRE-LENS.git
cd HIRE-LENS

# Install required Python packages
pip install -r requirements.txt
```

### 3. Run the Application

Launch the Streamlit web app:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🌐 Deploying to Streamlit Cloud

1. Push your project code to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial HireLens release"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/HIRE-LENS.git
   git push -u origin main
   ```
2. Log into [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub repository.
4. Set the main file path to `app.py`.
5. Click **Deploy!**

---

## 🔮 Future Enhancements

- [ ] LinkedIn Profile URL parsing & skill synchronization
- [ ] Cover Letter & AI Resume Rewriter Engine
- [ ] Recruiter Candidate Batch Screening Portal
- [ ] PostgreSQL cloud database migration

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.