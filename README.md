# FastAPI Backend for Render

## Features

- Upload PDF or DOCX and convert to LLM-friendly TXT
- CORS enabled for frontend integration

## Setup

1. Install dependencies (locally for testing):

   ```bash
   pip install -r requirements.txt
   ```

2. Run locally (for testing):
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 10000
   ```

## Deploy to Render

1. Push this backend folder to a GitHub repo.
2. Go to [Render](https://dashboard.render.com/) and create a new Web Service:
   - **Environment:** Python 3
   - **Build Command:** (leave blank or `pip install -r requirements.txt`)
   - **Start Command:**
     ```
     uvicorn main:app --host 0.0.0.0 --port 10000
     ```
   - **Port:** 10000
3. After deploy, use the Render URL in your frontend.
