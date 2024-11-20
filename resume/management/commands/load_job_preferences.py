import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from resume.models import JobPreference

class Command(BaseCommand):
    help = 'Load job preferences dataset into the database'

    def handle(self, *args, **kwargs):
        dataset_path = 'resume/data/job_preferences.csv'

        # Load the dataset
        data = pd.read_csv(dataset_path, encoding='ISO-8859-1')

        # Assign to a specific user (e.g., the first superuser or create a default user)
        default_user, _ = User.objects.get_or_create(
            username='default_user',
            email='default@example.com',
            defaults={'is_staff': True, 'is_superuser': True}
        )

        for _, row in data.iterrows():
            JobPreference.objects.create(
                user=default_user,  # Assign the default user
                job_title=row['job_title'],
                industry=row['industry'],
                skills=row['skills'],
                experience_level=row['experience_level'],
                job_description=row['job_description']
            )

        self.stdout.write(self.style.SUCCESS("Job preferences data loaded successfully!"))
