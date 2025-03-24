import sys
import os
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.pdf_processor import extract_text_from_pdf
from backend.test_case_generator import generate_test_cases

app = FastAPI()

# ✅ Fix: Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(pdf: UploadFile = File(...)):
    try:
        print("📂 Received PDF file:", pdf.filename)
        text = extract_text_from_pdf(pdf)
        print("✅ Extracted Text:", text[:100])  # Show only first 100 characters
        return {"text": text}
    except Exception as e:
        print("❌ Error extracting text:", e)
        return {"error": f"Error extracting text: {str(e)}"}

@app.post("/generate-test-cases")
async def generate_cases(data: dict):
    text = data.get("text", "").strip()

    if not text:
        return {"error": "No text provided for test case generation"}

    try:
        print("📝 Generating test cases for text:", text[:100])
        test_cases_json = generate_test_cases(text)
        test_cases = json.loads(test_cases_json)
        print("✅ Generated Test Cases:", test_cases)
        return {"test_cases": test_cases}
    except Exception as e:
        print("❌ Error generating test cases:", e)
        return {"error": f"Error generating test cases: {str(e)}"}
