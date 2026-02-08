from google import genai
from models import API_KEY, GENAI_PRO, GENAI_LITE
from google.genai import types
import json

def update_sections(resume_sections):
    with open('resume_updater/resume_updates.json', 'r') as file:
        global_system_instructions = json.load(file)

    client = genai.Client(api_key=API_KEY)

    sections = ['Contact', 'Experience', 'Projects', 'Education', 'Skills']
    updated_sections = []

    for section in sections:
        if section == 'Skills':
            resume_section_text = resume_sections
        else:
            resume_section_text = resume_sections[section.lower()]
        
        try:
            resume_section_text = json.dumps(resume_section_text, indent=4)
        except:
            continue

        system_instruction = f"""
                ### MASTER RULE
                Do not make up experiences, find a way to improve the section.
                If the section is already good and you don't see a need to improve it, then you do not need to change anything
                You can make up values if needed, but make sure the values are realistic, and needed for improvement
                
                ### Role
                You are a Resume Updater looking to improve someones resume one step at a time. The section you are focusing on is:

                {global_system_instructions[section]}

                If no information is found for a key in the json, assign the key None.

                INPUT:
                You will be given a dictionary of items with information in it, use the information as needed to fill out the output schema and provided imporvements where needed
            """

        response = client.models.generate_content(
            model=GENAI_LITE,
            contents=f'{resume_section_text}',
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=65000,
                system_instruction = system_instruction,
                response_mime_type = 'application/json',
            )
        ) 

        updated_sections.append(response.text)
    
    print(updated_sections)

    return updated_sections
            

