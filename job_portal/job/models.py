from django.db import models
from django.contrib.auth.models import User

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(upload_to='user_images/', null=True, blank=True)
    resume = models.FileField(upload_to='user_resumes/', null=True, blank=True)  
    type = models.CharField(max_length=15, default="student")

    def __str__(self):
        return self.user.username



class RecruiterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='recruiter_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

