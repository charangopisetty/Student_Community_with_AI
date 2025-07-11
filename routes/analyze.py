# backend/routes/analyze.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import requests
import os

router = APIRouter()

@router.post("/analyze/")
async def analyze_txt(file: UploadFile = File(...), prompt_template: str = Form(...)):
    txt_content = (await file.read()).decode('utf-8')
    prompt = prompt_template.format(txt=txt_content)
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return JSONResponse({"error": "Google API key not set"}, status_code=500)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return JSONResponse({"error": response.text}, status_code=response.status_code)
    try:
        ai_text = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        ai_text = response.text
    return {"result": ai_text}