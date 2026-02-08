from google import genai
from models import API_KEY, GENAI_PRO, GENAI_LITE
from google.genai import types 
import json

def extract_sections(text):
    client = genai.Client(api_key=API_KEY)

    system_instruction = """
            You are an expert Resume Parsing AI. Your task is to extract structured data from the provided resume text (which has been extracted from a DOCX file) and output strictly valid JSON.

            ### OUTPUT SCHEMA
            You must populate the following JSON structure. Do not alter the keys. Values can be None if they cannot be found.

            {
            "contact": { 
                "name": "Full Name", 
                "email": "extracted email", 
                "phone": "extracted phone", 
                "links": [], 
                "location": "City, State/Country" 
            },
            "summary": "Professional summary text",
            "education": [ 
                { 
                "school": "University Name", 
                "degree": "Degree Name", 
                "field": "Field of Study", 
                "start_date": "YYYY-MM or Present", 
                "end_date": "YYYY-MM or Present", 
                "location": "City, State", 
                "details": [] 
                } 
            ],
            "experience": [ 
                { 
                "company": "Company Name", 
                "title": "Job Title", 
                "location": "City, State", 
                "start_date": "YYYY-MM", 
                "end_date": "YYYY-MM or Present", 
                "bullets": [] 
                } 
            ],
            "projects": [ 
                { 
                "name": "Project Name", 
                "role": "Your Role", 
                "start_date": "YYYY-MM", 
                "end_date": "YYYY-MM", 
                "tech": [], 
                "bullets": [], 
                "link": "Project URL" 
                } 
            ],
            "skills": { 
                "languages": [], 
                "frameworks": [], 
                "tools": [], 
                "other": [] 
            },
            "certifications": [
                { "name": "Cert Name", "issuer": "Issuer", "date": "YYYY-MM" }
            ],
            "awards": [],
            "volunteering": [],
            "other_sections": {}
            }

            ### EXTRACTION RULES
            1. **Accuracy:** Do not hallucinate. If a field (like "links" or "location") is not found in the text, leave it as an empty string "" or empty array [].
            2. **Dates:** Attempt to normalize all dates to "YYYY-MM" format. If "Present" or "Current" is used, keep it as "Present".
            3. **Bullets:** Split paragraph text in Experience/Projects into individual bullet points strings.
            4. **Tech Stack:** Infer skills from the "Skills" section, but also extract mentioned technologies from project descriptions if they are explicit.
            5. **Formatting:** The input text is raw DOCX content; ignore page numbers, headers, or footers that interrupt the flow.
            6. **Output:** Return ONLY the JSON object. No markdown formatting (```json), no conversational text.

            ### MASTER RULES
            1. Return ONLY the JSON object. 
            2. Do not add conversational text like "Here is the JSON".
            3. If a field is missing, use None, do not enter empty variables such as '', [], or {}.
        """

    prompt = text

    # Define the schema to match your resume structure
    resume_schema = {
            "type": "OBJECT",
            "properties": {
                "contact": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING"},
                        "email": {"type": "STRING"},
                        "phone": {"type": "STRING"},
                        "links": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "location": {"type": "STRING"}
                    }
                },
                "summary": {"type": "STRING"},
                "education": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "school": {"type": "STRING"},
                            "degree": {"type": "STRING"},
                            "field": {"type": "STRING"},
                            "start_date": {"type": "STRING"},
                            "end_date": {"type": "STRING"},
                            "location": {"type": "STRING"},
                            "details": {"type": "ARRAY", "items": {"type": "STRING"}}
                        }
                    }
                },
                "experience": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "company": {"type": "STRING"},
                            "title": {"type": "STRING"},
                            "location": {"type": "STRING"},
                            "start_date": {"type": "STRING"},
                            "end_date": {"type": "STRING"},
                            "bullets": {"type": "ARRAY", "items": {"type": "STRING"}}
                        }
                    }
                },
                "projects": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "role": {"type": "STRING"},
                            "tech": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "bullets": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "link": {"type": "STRING"}
                        }
                    }
                },
                "skills": {
                    "type": "OBJECT",
                    "properties": {
                        "languages": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "frameworks": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "tools": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "other": {"type": "ARRAY", "items": {"type": "STRING"}}
                    }
                },
                "certifications": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "issuer": {"type": "STRING"},
                            "date": {"type": "STRING"}
                        }
                    }
                }
            }
        }

    # First API call with reasoning
    response = client.models.generate_content(
        model=GENAI_PRO,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=65000,
            system_instruction = system_instruction,
            response_mime_type = 'application/json',
            response_schema = resume_schema
        )
    ) 

    print(response.text)

    return json.loads(response.text)