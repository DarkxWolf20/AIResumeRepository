import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Resume Reviewer AI",
    page_icon="📄",
)

st.title("📄 Resume Reviewer AI")
st.write(
    "Upload a resume and get clear, practical feedback powered by AI."
)

st.info(
    "Prototype only: this reviews resume content. "
    "It is not a hiring or candidate-selection system."
)

api_key = st.text_input(
    "Gemini API key",
    type="password"
)
persona = st.text_input(
    "🎭 Choose your review persona",
    placeholder="e.g. That homeless guy outside that's constantly stoned, a medieval wizard, an angry chef..."
)
job_description = st.text_area(
    "🎯 Target job description (optional)",
    placeholder=(
        "Paste a job posting here to compare your resume "
        "with the role..."
    ),
    height=200
)

st.caption(
    "Optional: Add a job description to receive feedback "
    "tailored to that specific role."
)
st.caption(
    "Enter a fictional character, archetype, or personality. "
    "Leave blank for normal professional feedback."
)
uploaded_file = st.file_uploader(
    "Upload a resume",
    type=["pdf"]
)

if st.button("🔍 Review Resume", type="primary"):

    if not api_key:
        st.error("Please enter your Gemini API key.")
        st.stop()

    if not uploaded_file:
        st.error("Please upload a resume.")
        st.stop()

    try:
        client = genai.Client(api_key=api_key)
        resume_bytes = uploaded_file.getvalue()
        if job_description.strip():
            job_context = f"""
The user has also provided a target job description:

--- TARGET JOB DESCRIPTION ---
{job_description}
--- END TARGET JOB DESCRIPTION ---

Compare the resume with this specific job description in addition to
performing the normal resume review.

Include these additional sections:

## Job Alignment
Identify requirements or responsibilities from the job description
that are clearly supported by evidence in the resume.

## Gaps or Unclear Evidence
Identify important requirements from the job description that are not
clearly demonstrated in the resume.

Do NOT assume the person lacks these skills or qualifications.
Only state that the resume does not currently provide clear evidence
of them.

## Keywords & Terminology
Identify relevant terminology from the job description that could
appropriately appear in the resume if it truthfully describes the
person's experience.

Do not recommend keyword stuffing.

## Targeted Improvements
Suggest specific ways the resume could better communicate genuinely
relevant experience for this particular role.

Never invent qualifications, accomplishments, certifications,
experience, skills, or numbers simply to match the job description.
"""
        else:
            job_context = """
No target job description was provided.

Perform a general resume review only.
Do not include Job Alignment, Gaps or Unclear Evidence,
Keywords & Terminology, or Targeted Improvements sections.
"""
            prompt = f"""
You are a professional resume editor.

The user requested this persona for the presentation of the feedback:

"{persona if persona else "Professional Resume Coach"}"

{job_context}

Analyze the resume objectively before composing your response, but do
not output a separate objective analysis.

Your entire visible response must be written using the requested persona's
general personality, attitude, energy, humor, vocabulary, and communication
style from beginning to end.

Do not provide a normal professional review followed by a persona version.
There must be only ONE review and it HAS TO BE IN THE PERSONA stated.

The persona must affect the presentation of every section, including:
- Resume Snapshot
- Strengths
- Areas to Improve
- Rewrite Examples
- Quick Action Plan

The underlying observations must remain accurate and grounded in the
uploaded resume even though their presentation follows the persona.

IMPORTANT:
- The persona changes HOW the feedback is communicated, not the facts.
- Never change or invent resume information to fit the persona.
- Never invent accomplishments, numbers, experience, or qualifications.
- Keep all resume advice genuinely useful.
- If the persona is a recognizable fictional character, capture broad
  personality traits rather than copying distinctive dialogue or quotes.
- If the persona is unfamiliar, interpret the user's words as a requested
  communication style.

Review the uploaded resume for the quality of the resume itself.

The date is October 2026 btw.
"""

        with st.spinner("Reading and reviewing the resume..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    types.Part.from_bytes(
                        data=resume_bytes,
                        mime_type="application/pdf",
                    ),
                    prompt,
                ],
            )

        st.success("Resume reviewed!")
        st.markdown(response.text)

    except Exception as e:
        st.error("Something went wrong.")
        st.code(str(e))
        st.caption(
            "Check that your Gemini API key is correct "
            "and that the Gemini API is available for your account."
        )

st.divider()

st.caption(
    "Prototype only • Avoid uploading sensitive personal "
    "information while testing."
)
