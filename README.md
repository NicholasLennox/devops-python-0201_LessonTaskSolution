# Contacts API

A small API for managing contacts.

## Setup

Fork and clone the repository, then navigate to the project root.

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
# Can do the activation automatically when opening in VSCodes integrated terminal
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

## Running the app

```bash
python3 app.py
```

## Endpoints

- `GET /health`
- `GET /contacts`
- `GET /contacts/{id}`
- `POST /contacts`