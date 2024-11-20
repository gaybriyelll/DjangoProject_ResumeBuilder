from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import JobPreference
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class JobPreferenceForm(forms.ModelForm):
    job_description = forms.CharField(widget=forms.Textarea, required=False, label="Desired Job Description")

    class Meta:
        model = JobPreference
        fields = ['job_title', 'industry', 'skills', 'experience_level', 'job_description']

class FeedbackForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    comments = forms.CharField(widget=forms.Textarea, required=False)
