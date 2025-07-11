from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import pdfplumber
import io
import os
from docx import Document
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Allow CORS for frontend (adjust origin as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, set to your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file.file)
    elif ext == ".docx":
        text = extract_text_from_docx(file.file)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    formatted_text = format_for_llm(text)
    txt_bytes = io.BytesIO(formatted_text.encode("utf-8"))
    response = StreamingResponse(txt_bytes, media_type="text/plain")
    response.headers["Content-Disposition"] = f"attachment; filename={os.path.splitext(filename)[0]}.txt"
    return response

def extract_text_from_pdf(file_obj):
    text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_obj):
    doc = Document(file_obj)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def format_for_llm(text):
    headings = [
        "Experience", "Education", "Skills", "Projects", "Summary", "Contact", "Certifications", "Awards", "Interests", "Languages"
    ]
    for heading in headings:
        pattern = rf"(^|\n)\s*{heading}\s*:?\s*(\n|$)"
        repl = f"\n\n=== {heading.upper()} ===\n"
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    lines = text.splitlines()
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if re.match(r"^(\d+\.|[-*•])\s+", line):
            line = re.sub(r"^(\d+\.|[-*•])\s+", "- ", line)
        formatted_lines.append(line)
    formatted_text = "\n".join(formatted_lines)
    formatted_text = re.sub(r"\n{3,}", "\n\n", formatted_text)
    return formatted_text 