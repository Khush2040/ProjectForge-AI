# 🚀 ProjectForge AI

> **AI-Powered Software Project Planning Platform**

ProjectForge AI is an AI-powered software project planning platform that transforms raw software ideas into structured, implementation-ready project blueprints. Instead of directly generating code, it focuses on the planning stage of software development by analyzing project ideas, identifying requirements, recommending technologies, and producing a comprehensive software blueprint.

The long-term vision of ProjectForge AI is to become an AI Software Architect capable of planning, refining, retrieving, and eventually generating complete software systems.

---

## ✨ Features

### ✅ Current Features

- AI-powered project idea analysis
- Structured software project blueprint generation
- Automatic requirement extraction
- Technology stack recommendation
- Development roadmap generation
- Project blueprint storage in JSON format
- HuggingFace Embeddings generation
- Modular project architecture
- Streamlit-based UI (Work in Progress)

---

## 🚧 Upcoming Features

- FAISS Vector Database
- Semantic Project Search
- Retrieval-Augmented Generation (RAG)
- Interactive AI Project Consultant
- Project History Dashboard
- Architecture Diagram Generation
- Database Schema Suggestions
- API Planning Assistant
- Code Generation
- PDF & JSON Export
- Authentication & User Profiles

---

# 🏗️ Project Workflow

```text
User Project Idea
        │
        ▼
LangChain Prompt Template
        │
        ▼
Mistral AI
        │
        ▼
Structured Project Blueprint
        │
        ▼
Save JSON
        │
        ▼
Generate Embeddings
        │
        ▼
Semantic Search (Upcoming)
        │
        ▼
RAG (Upcoming)
        │
        ▼
Interactive AI Project Consultant
```

---

# 🧠 Example

### User Input

> Build an AI Interview Preparation Platform for Students

### ProjectForge AI Generates

- Project Overview
- Business Problem
- Objectives
- Functional Requirements
- Non-Functional Requirements
- Technology Stack
- Software Architecture
- Development Roadmap
- Risks
- Future Scope

---

# 🛠️ Tech Stack

### AI & Machine Learning

- LangChain
- Mistral AI
- HuggingFace Embeddings
- Sentence Transformers

### Backend

- Python

### Frontend

- Streamlit
- HTML
- CSS

### Data

- JSON

---

# 📂 Project Structure

```
ProjectForgeAI/
│
├── app.py
├── requirements.txt
├── .env
│
├── models/
│   └── llm.py
│
├── prompts/
│   └── project_prompt.py
│
├── services/
│   ├── project_analyzer.py
│   └── embedding_service.py
│
├── embeddings/
│   └── embedding_model.py
│
├── storage/
│   └── save_project.py
│
├── ui/
│   ├── styles.css
│   ├── components.py
│   └── animations.py
│
├── data/
│   └── projects.json
│
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/ProjectForgeAI.git
```

Navigate to the project

```bash
cd ProjectForgeAI
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.\.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
MISTRAL_API_KEY=your_api_key
```

Run the application

```bash
python -m streamlit run app.py
```

---

---

# 🎯 Vision

ProjectForge AI aims to become an AI-powered Software Architect that assists developers throughout the software development lifecycle—from project planning and architecture design to semantic search, intelligent retrieval, and automated code generation.

---
