# resume/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, JobPreferenceForm, FeedbackForm, LoginForm
from .models import Resume, JobPreference
from .nlp_model import generate_resume  # Assuming generate_resume function uses job description and skills
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def job_list(request):
    """List all job preferences"""
    job_preferences = JobPreference.objects.all()
    return render(request, 'resume/job_list.html', {'job_preferences': job_preferences})

def signup(request):
    """Sign up new users"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user after successful signup
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect('job_preference')  # Redirect to job preferences
    else:
        form = SignUpForm()

    return render(request, 'resume/signup.html', {'form': form})

def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')  # Redirect to job preferences after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'resume/login.html', {'form': form})

@login_required
def home(request):
    """Home page shown after login"""
    return render(request, 'resume/home.html')

@login_required
def job_preference(request):
    """Handle job preference form and generate resume"""
    if request.method == 'POST':
        form = JobPreferenceForm(request.POST)
        if form.is_valid():
            job_pref = form.save(commit=False)
            job_pref.user = request.user  # Associate job preference with the user
            job_pref.save()

            # Pass the job_pref object directly to generate_resume
            generated_resume = generate_resume(job_pref)

            # Save the generated resume to the database
            Resume.objects.create(
                user=job_pref.user,
                job_preference=job_pref,
                generated_resume=generated_resume
            )

            messages.success(request, "Resume generated successfully!")
            return redirect('resume_list')  # Redirect to the list of resumes
        else:
            messages.error(request, "There was an error with your form submission.")
    else:
        form = JobPreferenceForm()

    return render(request, 'resume/job_preference.html', {'form': form})

@login_required
def resume_list(request):
    """Display the list of resumes generated for the user"""
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'resume/resume_list.html', {'resumes': resumes})

@login_required
def feedback(request, resume_id):
    """Provide feedback on a specific resume"""
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        messages.error(request, "Resume not found.")
        return redirect('resume_list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Handle feedback saving logic here
            # feedback = form.save(commit=False)
            # feedback.resume = resume
            # feedback.save()
            messages.success(request, "Your feedback has been submitted.")
            return redirect('resume_list')
    else:
        form = FeedbackForm()

    return render(request, 'resume/feedback.html', {'form': form, 'resume': resume})

@login_required
def generate_pdf_resume(request, resume_id):
    """Generate a PDF resume based on job preferences and the generated resume content"""
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        messages.error(request, "Resume not found.")
        return redirect('resume_list')

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.job_preference.job_title}_resume.pdf"'

    # Create a PDF object using ReportLab
    p = canvas.Canvas(response, pagesize=letter)

    # Add content to the PDF
    p.drawString(100, 750, f"Resume for {resume.job_preference.job_title}")
    p.drawString(100, 730, f"Industry: {resume.job_preference.industry}")
    p.drawString(100, 710, f"Skills: {resume.job_preference.skills}")
    p.drawString(100, 690, f"Experience Level: {resume.job_preference.experience_level}")
    p.drawString(100, 670, f"Job Description: {resume.job_preference.job_description}")
    p.drawString(100, 650, f"Generated Resume: {resume.generated_resume}")

    # Save the PDF to the response object
    p.showPage()
    p.save()

    return response
