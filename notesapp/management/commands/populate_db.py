from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notesapp.models import Note
from faker import Faker


class Command(BaseCommand):
    help = "Populate DB with fake users and notes"

    def handle(self, *args, **kwargs):
        fake = Faker()
        NUM_USERS = 2000
        NOTES_PER_USER = 5

        for i in range(NUM_USERS):
            username = f'user{i+1}'
            email = f'{username}@example.com'

            # Avoid duplicates
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, email=email, password='password123')

                # Create notes for this user
                for _ in range(NOTES_PER_USER):
                    title = fake.sentence(nb_words=6)
                    content = fake.paragraph(nb_sentences=5)
                    Note.objects.create(
                        title=title, content=content, user=user)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {NUM_USERS} users with {NUM_USERS*NOTES_PER_USER} notes'))
