import spacy
import pandas as pd

# Load a pre-trained NLP model
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

# Simulated training dataset
data = pd.DataFrame({
    "job_title": ["Data Scientist", "Web Developer"],
    "skills": ["Python, Machine Learning, SQL", "HTML, CSS, JavaScript"],
    "resume_template": ["Optimized resume template for Data Scientist...", "Optimized resume template for Web Developer..."]
})

def train_model(data):
    # Dummy training logic for demonstration
    data['processed_skills'] = data['skills'].apply(preprocess_text)
    return data

trained_data = train_model(data)
trained_data.to_csv('trained_model.csv', index=False)
