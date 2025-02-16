from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)], null=True, blank=True)
    country = models.CharField(max_length=100)
    residence = models.CharField(max_length=100)


    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_timestamp = models.DateTimeField(blank=True, null=True)

    is_staff = None
    is_superuser = None
    last_login = None

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def projects_created_count(self):
        return self.projects.count()

    @property
    def projects_contributed_count(self):
        return self.contributed_projects.count()

class Skill(models.Model):
    LEVELS = [
        ('beginner', 'Beginner'),
        ('experienced', 'Experienced'),
        ('expert', 'Expert')
    ]

    LANGUAGES = [
        ('C++', 'C++'),
        ('Javascript', 'Javascript'),
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('Lua', 'Lua'),
        ('Rust', 'Rust'),
        ('Go', 'Go'),
        ('Julia', 'Julia')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    language = models.CharField(max_length=20, choices=LANGUAGES)
    level = models.CharField(max_length=20, choices=LEVELS)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'language'], name='unique_user_skill')
        ]

    def save(self, *args, **kwargs):
        if self.user.skills.count() >= 3:
            raise ValueError("A user can only have up to 3 skills.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.language} ({self.level})"

class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    max_collaborators = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.project_name

    @property
    def active_collaborators(self):
        """Returns the number of collaborators currently in the project."""
        return self.collaborators.count()

    @property
    def available_slots(self):
        """Calculates remaining slots for new collaborators."""
        return max(0, self.max_collaborators - self.active_collaborators)

    @property
    def is_open_for_collaboration(self):
        """Checks if the project is open for new collaborators."""
        return self.available_slots > 0

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="applications")
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'project'], name='unique_application')
        ]

    def __str__(self):
        return f"{self.applicant.username} applied for {self.project.project_name} ({self.status})"

    def accept(self):
        """Accepts an application and adds the user to collaborators if slots are available."""
        if self.project.available_slots > 0 and not self.project.collaborators.filter(user=self.applicant).exists():
            self.status = 'accepted'
            self.save()
            Collaborator.objects.get_or_create(user=self.applicant, project=self.project)
        else:
            raise ValueError("Project has reached max collaborators or user is already a collaborator.")

    def decline(self):
        """Declines an application."""
        self.status = 'declined'
        self.save()

class Collaborator(models.Model):
    """Tracks which users are collaborating on which projects."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collaborators")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborations")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'user'], name='unique_collaboration')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name}"
