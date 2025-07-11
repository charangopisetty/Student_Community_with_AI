from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

@router.post("/build-website/")
async def build_website(file: UploadFile = File(...), prompt_template: str = Form(...)):
    # Read the content of the uploaded prompt .txt file
    prompt_content = (await file.read()).decode('utf-8')
    # Combine with your second prompt
    prompt = prompt_template.format(content=prompt_content)
    # Example: Use OpenAI API (or Gemini, similar to previous step)
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        return JSONResponse({"error": "OpenAI API key not set"}, status_code=500)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",  # or "gpt-4", "gpt-3.5-turbo", etc.
        "messages": [
            {"role": "system", "content": "You are an expert website builder AI."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return JSONResponse({"error": response.text}, status_code=response.status_code)
    try:
        website_code = response.json()['choices'][0]['message']['content']
    except Exception:
        website_code = response.text
    return {"result": website_code}