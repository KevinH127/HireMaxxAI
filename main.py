from original_resume_extraction.docx_extractor import extract_docx_to_text
from original_resume_extraction.sections_extractor import extract_sections
import json

PDF_PATH = "KevinHuang_Resume2026.pdf"

text = extract_docx_to_text(PDF_PATH)

sections = extract_sections(text)

print(json.dumps(sections, indent=4))