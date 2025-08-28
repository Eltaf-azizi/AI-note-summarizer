<h1 align="center">AI Note Summarizer</h1>

An intelligent note summarization app that uses Natural Language Processing (NLP) and Transformer models to automatically summarize long pieces of text into concise, easy-to-read notes.


## 🚀 Features

 - 📄 **Text Summarization** – Condense large amounts of text into short summaries.
 - 🧩 **Chunking Pipeline** – Handles long text by splitting it into smaller sections before summarization.
 - ⚡**Fast API with Flask** – Lightweight web application with a clean UI.
 - 🎨 **Responsive Design** – Simple, minimal frontend with HTML & CSS.
 - 🧪 **Testing Suite** – Includes unit tests for core modules and pipelines.
 - 🐳 **Docker Support** – Containerized for easy deployment.
 - ☁️ **Cloud Ready** – Procfile and Gunicorn configuration for deployment on platforms like Heroku.

## Project Structure

    AI-Note-Summarizer/
    ├─ README.md                # Documentation
    ├─ requirements.txt         # Python dependencies
    ├─ .gitignore               # Ignored files
    ├─ LICENSE                  # License file
    ├─ .env.example             # Example environment variables
    ├─ Dockerfile               # Docker container setup
    ├─ gunicorn.conf.py         # Gunicorn configuration
    ├─ Procfile                 # Deployment file (Heroku)
    │
    ├─ src/                     # Application source code
    │  ├─ app.py                # Flask app entry point
    │  ├─ config.py             # Configuration management
    │  ├─ summarizer.py         # Summarization logic
    │  ├─ pipeline.py           # Text preprocessing & chunking pipeline
    │  ├─ utils.py              # Utility functions
    │  └─ __init__.py
    │
    ├─ templates/               # Frontend templates
    │  └─ index.html
    │
    ├─ static/                  # Static assets
    │  └─ style.css
    │
    ├─ tests/                   # Unit tests
    │  ├─ test_chunking.py
    │  ├─ test_pipeline_mock.py
    │  └─ conftest.py
    │
    └─ .github/
       └─ workflows/
      └─ ci.yml             # GitHub Actions CI workflow

## ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/yourusername/aibrief.git
cd aibrief
```

### 2. Create a virtual environment & install dependencies

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```


