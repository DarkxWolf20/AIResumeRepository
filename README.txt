RESUME REVIEWER AI — PROTOTYPE

WHAT IT DOES
1. Opens a webpage.
2. Lets you upload a PDF, DOCX, or TXT resume.
3. Sends the document to an OpenAI model.
4. Displays structured resume feedback.

YOU NEED
- Python 3.10+ recommended
- An OpenAI API key with API access/credits

RUN IT — WINDOWS
Open Command Prompt or PowerShell in this folder:

py -m pip install -r requirements.txt
py -m streamlit run app.py

RUN IT — MAC
Open Terminal in this folder:

python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py

Then enter your API key, upload the sample resume, and click Review Resume.

IMPORTANT
Do not put your API key into the source code or publish it to GitHub.
This prototype is for resume-writing feedback, not hiring decisions.
