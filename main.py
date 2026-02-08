from original_resume_extraction.docx_extractor import extract_docx_to_text
from original_resume_extraction.sections_extractor import extract_sections
from resume_updater.sections_updater import update_sections
from resume_updater.resume_formatter import update_resume

PDF_PATH = "KevinHuang_Resume2026.pdf"

text = extract_docx_to_text(PDF_PATH)

sections = extract_sections(text)

updated_sections = update_sections(sections)

updated_resume = update_resume(updated_sections)

print(updated_resume)