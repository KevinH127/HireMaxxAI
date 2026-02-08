from google import genai
from google.genai import types
from models import API_KEY, GENAI_PRO
import json


def update_resume(sections):
    client = genai.Client(api_key=API_KEY)

    system_instruction = r"""
            ### ROLE
            You are an expert LaTeX Resume Formatter. I will provide you with resume content divided into 5 sections: Contact, Experience, Projects, Education, and Skills.
            
            ### TASK
            Your task is to take this information and input it into the LaTeX template provided at the bottom of this prompt.
            
            ### Strict Rules:
            1. Content Fidelity: Only use the content provided in my input. Do not hallucinate or add information that is not there.
            2. Professional Review: Perform a final check on the provided content to ensure every bullet point makes sense, is grammatically correct, and sounds professional and formal.
            
            ### Formatting:
            1. Font: The entire document must use Times New Roman.
            2. Name: Must be on its own single line at the top.
            3. Contact Info: Must be on a single line below the name.
            4. Length: The resume must fit strictly on one page. If the content provided is too long, you are authorized to reduce `\vspace` values or use `\small` for bullet points to ensure it does not spill onto a second page.
            5. If the content exceeds one page, prioritize removing the oldest project or shortening the summary before providing the code.
            
            ### STRICT Output: 
            The output must be only the raw LaTeX code. Do not include markdown code blocks (```latex), explanations, or conversational text. Just the code.

            Here is the LaTeX Template to use:
            %-------------------------
            % Resume in Latex
            % Author : HireMaxxAI
            % Based off of: [https://github.com/jakeryang/resume](https://github.com/jakeryang/resume)
            % License : MIT
            %------------------------

            \documentclass[letterpaper,10pt]{article} % Changed to 10pt to assist with 1-page fit

            \usepackage{latexsym}
            \usepackage[empty]{fullpage}
            \usepackage{titlesec}
            \usepackage{marvosym}
            \usepackage[usenames,dvipsnames]{color}
            \usepackage{verbatim}
            \usepackage{enumitem}
            \usepackage[hidelinks]{hyperref}
            \usepackage{fancyhdr}
            \usepackage[english]{babel}
            \usepackage{tabularx}
            \usepackage{fontawesome5}
            \usepackage{multicol}
            \setlength{\multicolsep}{-3.0pt}
            \setlength{\columnsep}{-1pt}

            % Times New Roman Font Setup
            \usepackage[T1]{fontenc}
            \usepackage{newtxtext,newtxmath} 

            \pagestyle{fancy}
            \fancyhf{} 
            \fancyfoot{}
            \renewcommand{\headrulewidth}{0pt}
            \renewcommand{\footrulewidth}{0pt}

            % Adjust margins for maximum space
            \addtolength{\oddsidemargin}{-0.5in}
            \addtolength{\evensidemargin}{0in}
            \addtolength{\textwidth}{1in}
            \addtolength{\topmargin}{-.5in}
            \addtolength{\textheight}{1.0in}

            \urlstyle{same}
            \raggedbottom
            \raggedright
            \setlength{\tabcolsep}{0in}

            % Section formatting
            \titleformat {\section}{
                \bfseries \vspace{2pt} \raggedright \large 
            }{}{0em}{}[\color{light-grey} {\titlerule[1.5pt]} \vspace{-4pt}]

            \definecolor{light-grey}{gray}{0.83}
            \definecolor{dark-grey}{gray}{0.3}
            \definecolor{text-grey}{gray}{.08}

            % Custom commands
            \newcommand{\resumeItem}[1]{
            \item\small{
                {#1 \vspace{-1.5pt}}
            }
            }

            \newcommand{\resumeSubheading}[4]{
            \vspace{-1pt}\item
                \begin{tabular*}{\textwidth}[t]{  l@  {\extracolsep{\fill}}r}
                \textbf{#1} & {\small #2}\vspace{1pt}\\ 
                \textit{#3} & {\small #4}\\ 
                \end{tabular*}\vspace{-6pt}
            }

            \newcommand{\resumeProjectHeading}[2]{
                \item
                \begin{tabular*}{\textwidth}{  l@  {\extracolsep{\fill}}r}
                #1 & {\small #2} 
                \end{tabular*}\vspace{-6pt}
            }

            \newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
            \newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-4pt}}
            \newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in]}
            \newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-2pt}}

            \color{text-grey}

            \begin{document}

            \begin{center}
                \textbf{\Huge INSERT NAME HERE} \\ \vspace{2pt}
                \small 
                \faPhone* \texttt{PHONE} \hspace{1pt} | \hspace{1pt} 
                \faEnvelope \hspace{2pt} \texttt{EMAIL} \hspace{1pt} | \hspace{1pt} 
                \faLinkedin \hspace{2pt} \texttt{LINKEDIN/PORTFOLIO} \hspace{1pt} | \hspace{1pt} 
                \faMapMarker* \hspace{2pt}\texttt{LOCATION}
                \vspace{-8pt}
            \end{center}

            \section{EXPERIENCE}
            \resumeSubHeadingListStart
                % Loop Experience Items here
            \resumeSubHeadingListEnd

            \section{PROJECTS}
            \resumeSubHeadingListStart
                % Loop Project Items here
            \resumeSubHeadingListEnd

            \section{EDUCATION}
            \resumeSubHeadingListStart
                % Loop Education Items here
            \resumeSubHeadingListEnd

            \section{SKILLS}
            \begin{itemize}[leftmargin=0in, label={}]
                \small{\item{
                % Insert Skills Category format
                }}
            \end{itemize}

            \end{document}
        """
    response = client.models.generate_content(
            model=GENAI_PRO,
            contents=f'{sections}',
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=65000,
                system_instruction = system_instruction,
                response_mime_type = 'text/plain',
            )
        ) 

    return response.text