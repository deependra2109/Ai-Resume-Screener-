# 🤖 AI Resume Screener

> **An AI-powered resume analysis platform that evaluates resumes against job descriptions, identifies skill gaps, provides ATS-focused insights, and helps candidates improve their resumes.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📌 Overview

**AI Resume Screener** is a resume analysis application designed to help candidates understand how well their resume aligns with a specific job description.

Instead of relying only on keyword matching, the application combines **semantic similarity, skill matching, and LLM-based analysis** to provide a more detailed evaluation of a candidate's resume.

The application can extract content from PDF resumes, compare it with a job description, identify relevant and missing skills, generate ATS-oriented feedback, suggest resume improvements, and create a tailored cover letter.

The project was built to explore how **NLP, semantic analysis, and Large Language Models can be combined with a practical recruitment-oriented application.**

---

## ✨ Key Features

### 📄 Resume Parsing
- Upload a resume in PDF format
- Extract text from the uploaded document
- Preprocess extracted content for analysis
- Analyze resume content against a target job description

### 🧠 Semantic Resume Matching

The application uses semantic similarity to understand the relationship between resume content and job requirements rather than depending entirely on exact keyword matches.

This helps identify relevant experience even when the resume and job description use different wording.

### 🛠️ Skill Matching

Analyze the relationship between:

- Skills present in the resume
- Skills mentioned in the job description
- Matching skills
- Missing or potentially relevant skills

This gives candidates a clearer picture of where their resume aligns with the target role.

### 🤖 AI-Powered Analysis

Google Gemini is used for higher-level resume analysis and generation tasks.

The AI layer can provide insights such as:

- Resume strengths
- Potential weaknesses
- Job-specific gaps
- Improvement suggestions
- ATS-oriented recommendations

### 📊 ATS Analysis

The project provides an ATS-focused analysis of the resume and job description, helping candidates identify areas that may affect how effectively their resume communicates relevant qualifications.

### ✍️ Resume Optimization

Generate targeted suggestions for improving resume content based on the target job description.

The goal is not to blindly insert keywords, but to make relevant experience and skills clearer and more aligned with the role.

### 📨 Cover Letter Generation

Generate a job-specific cover letter using the candidate's resume information and target job description.

### 🎨 Streamlit Interface

A clean web-based interface built with Streamlit provides access to the complete analysis workflow without requiring users to interact directly with the backend code.

---

# 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │       Streamlit      │
                    │         UI           │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │     Application      │
                    │       Layer          │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌──────────────┐  ┌──────────────┐
      │ PDF         │   │ Text         │  │ Skill        │
      │ Extraction  │   │ Processing   │  │ Matching     │
      └──────┬──────┘   └──────┬───────┘  └──────┬───────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Semantic Similarity  │
                    │      Analysis        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Gemini / LLM     │
                    │      Analysis        │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼───────────────┐
                ▼              ▼               ▼
          ┌───────────┐ ┌────────────┐ ┌──────────────┐
          │ ATS       │ │ Resume     │ │ Cover Letter │
          │ Analysis  │ │ Optimizer  │ │ Generator    │
          └─────┬─────┘ └─────┬──────┘ └──────┬───────┘
                │             │               │
                └─────────────┼───────────────┘
                              ▼
                    ┌──────────────────────┐
                    │    Results & UI      │
                    └──────────────────────┘
```

---

# 📂 Project Structure

```text
resume_screener/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
│
├── core/
│   ├── __init__.py
│   ├── pdf_extractor.py
│   ├── similarity.py
│   ├── skill_matcher.py
│   └── text_preprocessing.py
│
├── llm/
│   ├── __init__.py
│   ├── ats_analysis.py
│   ├── cover_letter.py
│   ├── gemini_client.py
│   └── resume_optimizer.py
│
├── ui/
│   ├── __init__.py
│   ├── results_view.py
│   ├── sidebar.py
│   ├── styles.py
│   └── theme.py
│
├── .streamlit/
│   └── config.toml
│
└── README.md
```

---

# 🔍 How It Works

The application follows a multi-stage analysis pipeline.

### 1. Upload Resume

The user uploads a resume in PDF format.

### 2. Extract Resume Text

The PDF extraction layer extracts the textual content required for further processing.

### 3. Preprocess Text

The extracted content is cleaned and prepared for downstream analysis.

### 4. Analyze Job Description

The target job description is processed to identify important requirements and skills.

### 5. Calculate Semantic Similarity

Resume content and job requirements are compared using semantic similarity techniques.

This allows the system to identify conceptual relationships beyond simple exact keyword matches.

### 6. Match Skills

The skill-matching layer identifies relevant skills appearing in both the resume and target job description.

### 7. Generate AI Analysis

The Gemini-powered LLM layer analyzes the resume and job requirements to provide higher-level insights.

### 8. Generate Results

The application presents analysis through the Streamlit interface, including ATS insights, skill gaps, optimization suggestions, and generated content.

---
Screenshots
<img width="1237" height="537" alt="11" src="https://github.com/user-attachments/assets/46f28d41-6432-467d-abf6-206fe6b258a2" />
<img width="1249" height="652" alt="22" src="https://github.com/user-attachments/assets/a0d4a278-7a69-41fc-89bc-1307cd5900b3" />
<img width="1600" height="807" alt="33" src="https://github.com/user-attachments/assets/a0790e66-72ad-4191-89e4-16f7fa124364" />




# 🧠 AI & NLP Components

The project combines multiple approaches rather than depending on a single AI technique.

| Component | Purpose |
|---|---|
| PDF Extraction | Extract text from resumes |
| Text Preprocessing | Clean and prepare text |
| Semantic Similarity | Compare resume and job requirements semantically |
| Skill Matching | Identify matching and missing skills |
| Google Gemini | Perform contextual LLM-based analysis |
| ATS Analysis | Provide ATS-focused resume insights |
| Resume Optimizer | Generate targeted improvement suggestions |
| Cover Letter Generator | Generate job-specific cover letters |

---

# 🛠️ Tech Stack

### Core

- **Python**
- **Streamlit**
- **PDF processing**
- **NLP / semantic analysis**

### AI

- **Google Gemini**
- **Semantic embeddings / similarity analysis**
- **LLM-based resume analysis**

### Frontend

- Streamlit
- Custom CSS
- Custom UI components

### Development

- Git
- GitHub
