import pdfplumber

def extract_docx_to_text(PDF_PATH):
    with pdfplumber.open(PDF_PATH) as pdf:
        all_text = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            all_text.append(text)
            print(f"\n--- PAGE {i+1} ---\n")
            print(text)

    full_text = "\n\n".join(all_text)

    print("\n=== FULL TEXT LENGTH ===")
    return full_text
