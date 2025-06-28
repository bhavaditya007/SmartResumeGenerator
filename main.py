    import streamlit as st
import google.generativeai as genai

# Configure your Gemini API key here
api_key = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain"
}

def clean_resume_text(text):
    text = text.replace("[Add Email Address]", "[Your Email Address]")
    text = text.replace("[Add Phone Number]", "[Your Phone Number]")
    text = text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    text = text.replace("[University Name]", "[Your University Name]")
    text = text.replace("[Graduation Year]", "[Your Graduation Year]")
    return text

def generate_resume(name, job_title):
    context = (
        f"Generate a professional resume for {name} applying for the job title '{job_title}'. "
        "Include sections like Professional Summary, Experience, Education, and Skills. "
        "Use dummy projects and experience if needed, and format the output in Markdown."
    )
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
    chat_session = model.start_chat(history=[{"role": "user", "parts": [context]}])
    response = chat_session.send_message(context)
    if hasattr(response, 'text') and isinstance(response.text, str):
        text = response.text
    else:
        text = response.parts[0].text
    return clean_resume_text(text)

st.title("SmartResume Generator")
st.write("Create a professional, AI-generated resume tailored to your needs.")

name = st.text_input("Enter your name")
job_title = st.text_input("Enter your desired job title")

if st.button("Generate Resume"):
    if name and job_title:
        with st.spinner("Generating your resume..."):
            resume = generate_resume(name, job_title)
        st.markdown(resume)
        st.download_button("Download Resume", resume, file_name=f"{name}_resume.md")
    else:
        st.warning("Please enter both your name and job title.")
