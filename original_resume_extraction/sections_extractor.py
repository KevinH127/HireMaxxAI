from openai import OpenAI
from models import API_KEY, GENAI_PRO
import json

def extract_sections(text):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    )

    SECTION_SCHEMA = """
            {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "key_points": {"type": "array", "items": {"type": "string"}},
                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]}
            }
            }
        """

    system_instruction = """
            You are an expert Resume Parsing AI. Your task is to extract structured data from the provided resume text (which has been extracted from a DOCX file) and output strictly valid JSON.

            ### OUTPUT SCHEMA
            You must populate the following JSON structure. Do not alter the keys. Values can be None if they cannot be found.

            {
            "contact": { 
                "name": "Full Name", 
                "email": "extracted email", 
                "phone": "extracted phone", 
                "links": ["url1", "url2"], 
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
                "details": ["Honors", "GPA", "Relevant Coursework"] 
                } 
            ],
            "experience": [ 
                { 
                "company": "Company Name", 
                "title": "Job Title", 
                "location": "City, State", 
                "start_date": "YYYY-MM", 
                "end_date": "YYYY-MM or Present", 
                "bullets": ["Responsibility 1", "Achievement 2"] 
                } 
            ],
            "projects": [ 
                { 
                "name": "Project Name", 
                "role": "Your Role", 
                "start_date": "YYYY-MM", 
                "end_date": "YYYY-MM", 
                "tech": ["Python", "React", "AWS"], 
                "bullets": ["Description of project"], 
                "link": "Project URL" 
                } 
            ],
            "skills": { 
                "languages": ["Python", "JavaScript"], 
                "frameworks": ["Django", "React"], 
                "tools": ["Git", "Docker"], 
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
            3. If a field is missing, use empty strings "" or lists [].
        """

    prompt = text

    # First API call with reasoning
    response = client.chat.completions.create(
        model=GENAI_PRO,
        messages=[
                {
                    "role" : "system",
                    "content" : system_instruction
                },
                {
                    "role": "user",
                    "content": prompt
                }
        ],
        response_format = {"type": "json_object"} 
    )

    # Extract the assistant message with reasoning_details
    response = response.choices[0].message.content
    response = json.loads(response)

    return response