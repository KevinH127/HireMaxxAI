# HireMaxAI

HireMaxAI is an AI-powered resume analysis tool that helps users optimize their resumes for applicant tracking systems (ATS) and recruiters.

Think of it as resume “looksmaxxing”: identify weak points, improve alignment, and maximize interview potential.

---

## Problem

Most resumes fail before reaching a human reviewer.

Common issues:
- Poor keyword alignment with job descriptions
- Weak or vague bullet points
- Generic resumes not tailored to specific roles

Applicants rarely know what changes actually matter.

---

## Solution

HireMaxAI analyzes a resume against a job description and returns:
- An ATS match score
- Ranked, high-impact improvement suggestions
- Rewritten resume bullets optimized for clarity and impact

The goal is actionable feedback, not generic advice.

---

## Core Features (MVP)

- ATS Match Scoring (0–100)
- Resume-to-job-description keyword analysis
- Bullet point rewriting with quantified impact
- Structured resume parsing from PDF files
- Output in structured JSON format

---

## How It Works

1. Parse resume PDF into structured sections (Education, Experience, Skills, Projects)
2. Analyze job description for required skills and keywords
3. Compare resume content against job requirements
4. Generate prioritized fixes and rewritten bullets

---

## Tech Stack

- Frontend: React / Next.js
- Backend: Python
- AI: Large Language Model (LLM)
- PDF Parsing: pdfplumber
- Data Output: Python dictionary and JSON

---

## Getting Started

Follow these instructions to run the project locally.

### Prerequisites

- Python 3.10+
- Node.js & npm
- **Gemini API Key** (You need a Google Gemin API key)

### 1. Backend Setup

The backend handles the resume parsing, AI analysis, and PDF generation.

1.  **Navigate to the project root.**

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Tectonic (LaTeX Engine):**
    The backend uses `tectonic` to compile the generated LaTeX resume into a PDF.
    ```bash
    # macOS / Linux
    curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net |sh
    ```
    *Ensure the `tectonic` binary is in the project root or in your system PATH.*

5.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add your API key to it:
    ```env
    API_KEY=your_google_gemini_api_key
    ```
    *Note: The frontend also uses the same key for some operations, ensure `.env.local` in `frontend/` is also set up if needed, though mostly the backend handles the heavy lifting now.*

6.  **Run the Backend Server:**
    ```bash
    python backend_server.py
    ```
    The server will start on `http://0.0.0.0:8000`.

### 2. Frontend Setup

The frontend is a React application styled with Tailwind CSS.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    The application will handle proxying API requests to the backend automatically.

4.  **Open the App:**
    Visit `http://localhost:3000` (or the URL shown in your terminal) in your browser.

---

## Usage

1.  Start both the Backend and Frontend servers.
2.  Open the web app.
3.  Upload your existing Resume (PDF format).
4.  Wait for the AI to analyze, rewrite, and reformat your resume (~2 minutes).
5.  Preview the result and download your new **Perfected Resume** as a PDF.
