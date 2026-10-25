from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.question}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option

class Participant(models.Model):
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    institution = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class QuizResult(models.Model):
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.quiz.title}: {self.score}/{self.total_questions}"