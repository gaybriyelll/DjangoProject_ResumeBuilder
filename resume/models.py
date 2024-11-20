from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

class JobPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    skills = models.TextField()
    experience_level = models.CharField(max_length=50)
    job_description = models.TextField(blank=True, null=True)  # Optional field for job description

    def __str__(self):
        return f"{self.job_title} in {self.industry}"

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_preference = models.ForeignKey(JobPreference, on_delete=models.CASCADE)
    generated_resume = models.TextField()
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume for {self.user.username} ({self.job_preference.job_title})"
    
    def save(self, *args, **kwargs):
        # Automatically increment the version for each new resume
        if not self.pk:  # Only run this logic if it's a new instance
            latest_version = Resume.objects.filter(user=self.user).aggregate(Max('version'))['version__max']
            self.version = latest_version + 1 if latest_version is not None else 1  # Start from version 1 if no resume exists
        super().save(*args, **kwargs)
