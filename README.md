# Critical Information Redactor

A web application that redacts sensitive information from documents using spaCy NLP and regex-based strategies.

## Features

- Redacts **names**, **emails**, and **phone numbers** from uploaded documents
- Two redaction strategies:
  - **NLP** (spaCy): detects names, emails, and phone numbers using a language model
  - **Regex**: detects emails and phone numbers using pattern matching
- Supports plain text files, PDF and DOCX are in progress 
- Simple localhost web interface

## Getting Started

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the application

```bash
python main.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. Open the web interface in your browser.
2. Upload a document (TXT).
3. Select a redaction strategy (**NLP** or **Regex**).
4. Choose which fields to redact (Name, Email, Phone number).
5. Download or view the redacted output.

## Project Structure

```
.
├── main.py                  # Application entry point
├── requirements.txt
├── pipeline/
│   ├── extractor.py         # Extracts text from uploaded files
│   ├── redactor.py          # Orchestrates redaction strategies
│   ├── reconstructor.py     # Rebuilds output from redacted text
│   └── strategies/
│       ├── regex.py         # Regex-based redactors
│       └── spacy.py         # spaCy NLP-based redactors
├── webpage/
│   ├── webpage_interface.py # Flask routes
│   ├── index.html
│   └── results.html
└── buffer/                  # Temporary storage for uploaded files
```

## Requirements

- Python 3.9+
- See [requirements.txt](requirements.txt) for full dependency list
