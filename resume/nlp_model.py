# nlp_model.py

def generate_resume(job_preference):
    """Generate a resume based on the user's job preference."""
    resume_text = f"Resume for {job_preference.user.username}\n"
    resume_text += f"Job Title: {job_preference.job_title}\n"
    resume_text += f"Industry: {job_preference.industry}\n"
    resume_text += f"Skills: {job_preference.skills}\n"
    resume_text += f"Experience Level: {job_preference.experience_level}\n"
    
    # Check if job description exists
    if job_preference.job_description:
        resume_text += f"Job Description: {job_preference.job_description}\n"
    
    resume_text += "\n\n---\nGenerated Resume based on NLP model"
    
    return resume_text
