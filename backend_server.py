from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from original_resume_extraction.docx_extractor import extract_docx_to_text
from original_resume_extraction.sections_extractor import extract_sections
from resume_updater.sections_updater import update_sections
from resume_updater.resume_formatter import update_resume
import shutil
import os
import uvicorn
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    temp_file = f"temp_{file.filename}"
    tex_file = "output.tex"
    pdf_file = "output.pdf"
    
    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print("Extracting text...")
        text = extract_docx_to_text(temp_file)
        
        print("Extracting sections...")
        sections = extract_sections(text)
        
        print("Updating sections...")
        # update_sections logic involves iterating and calling Gemini
        updated_sections = update_sections(sections)
        
        print("Formatting resume...")
        updated_resume = update_resume(updated_sections)
        
        # Save Latex
        with open(tex_file, "w") as f:
            f.write(updated_resume)
        
        print("Compiling PDF with Tectonic...")
        # Use ./tectonic if it exists in current dir, or just tectonic if in path
        tectonic_cmd = "./tectonic" if os.path.exists("./tectonic") else "tectonic"
        
        subprocess.run([tectonic_cmd, tex_file], check=True)
        
        if not os.path.exists(pdf_file):
             raise HTTPException(status_code=500, detail="PDF generation failed")
             
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
            
        return Response(content=pdf_bytes, media_type="application/pdf")
        
    except subprocess.CalledProcessError as e:
        print(f"Tectonic error: {e}")
        # If compilation fails, maybe return the latex as a fallback or just error?
        # For now error.
        raise HTTPException(status_code=500, detail="LaTeX compilation failed")
        
    except Exception as e:
        print(f"Error processing resume: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        for f in [temp_file, tex_file, pdf_file]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
