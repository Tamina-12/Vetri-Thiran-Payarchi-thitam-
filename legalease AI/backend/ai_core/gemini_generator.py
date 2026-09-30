import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if self.api_key:
            self.client = genai.Client(
                api_key=self.api_key
            )
        else:
            self.client = None

    def generate(self, prompt: str) -> str:

        if not prompt.strip():
            return "Please provide a prompt."

        if self.client:
            try:
                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as e:
                print(
                    "Gemini unavailable. "
                    "Using local fallback."
                )
                print(e)

        return self.fallback_document(prompt)

    def fallback_document(self, prompt: str) -> str:

        return """
STUDENT PROJECT AGREEMENT

1. PARTIES

This agreement is made between the student and the project
guide/institution for the purpose of completing an academic
project.

2. PROJECT RESPONSIBILITIES

The student agrees to complete the assigned project work
according to the requirements and instructions provided by
the project guide.

3. PROJECT WORK

The student will carry out the project activities, prepare
the required documentation, and submit the completed work
within the academic schedule.

4. CONFIDENTIALITY

Any confidential academic, institutional, or project-related
information shared during the project should be handled
responsibly and should not be disclosed without permission.

5. COMPLETION

The student agrees to make reasonable efforts to complete
the project and submit the required deliverables.

6. EFFECTIVE DATE

This agreement becomes effective on the date specified by
the parties.

7. SIGNATURES

Student Name: __________________________

Student Signature: _____________________

Project Guide: _________________________

Guide Signature: _______________________

Date: __________________________________
"""

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str
    ) -> str:

        prompt = f"""
Create a professional academic legal document.

Document Type:
{document_type}

Parties:
{parties}

Terms:
{terms}

Effective Date:
{effective_date}

Use clear professional language, headings,
and signature sections.
"""

        return self.generate(prompt)