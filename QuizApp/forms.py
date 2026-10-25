from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Your Username or Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Your Password'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username_or_email and password:
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    raise forms.ValidationError('Invalid username or email.')
            else:
                username = username_or_email
            self.user_cache = authenticate(
                self.request,
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError('Invalid username/email or password.')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Old Password'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input New Password'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Confirm Password'}))

class QuizForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Quiz Title'}))
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Input Quiz Description...'}))

    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Input your question text here...'}))

    class Meta:
        model = Question
        fields = ['question']

class OptionForm(forms.ModelForm):
    option = forms.CharField(label='Option Text', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input option text (e.g., Python, Java)'}))
    is_correct = forms.BooleanField(label='Is this the correct answer?', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input ms-1'}))

    class Meta:
        model = Option
        fields = ['option', 'is_correct']

class ParticipantForm(forms.ModelForm):
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Full Name'}))
    student_class = forms.CharField(label='Class/Grade', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Class (e.g. Class 10)'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Input Age'}))
    gender = forms.ChoiceField(choices=Participant.GENDER_CHOICES, label='Gender', widget=forms.Select(attrs={'class': 'form-select'}))
    institution = forms.CharField(label='Institution', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input School/College Name'}))

    class Meta:
        model = Participant
        fields = ['name', 'student_class', 'age', 'gender', 'institution']