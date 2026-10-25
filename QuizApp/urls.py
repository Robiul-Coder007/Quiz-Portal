from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='user_login'),
    path('register/', register, name='register'),
    path('change-password/', change_pass, name='change_pass'),
    path('logout/', user_logout, name='user_logout'),

    path('participant/', participant, name='participant'),
    path('dashboard/', dashboard, name='dashboard'),

    path('quiz/add/', add_quiz, name='add_quiz'),
    path('quiz/detail/<int:pk>/', quiz_detail, name='quiz_detail'),
    path('quiz/edit/<int:pk>/', update_quiz, name='update_quiz'),
    path('quiz/delete/<int:pk>/', delete_quiz, name='delete_quiz'),

    path('quiz/<int:quiz_id>/question/add/', add_question, name='add_question'),
    path('question/edit/<int:pk>/', update_question, name='update_question'),
    path('question/delete/<int:pk>/', delete_question, name='delete_question'),

    path('question/<int:question_id>/option/add/', add_option, name='add_option'),
    path('option/edit/<int:pk>/', update_option, name='update_option'),
    path('option/delete/<int:pk>/', delete_option, name='delete_option'),

    path('quiz/start/<int:quiz_id>/', start_quiz, name='start_quiz'),
    path('quiz/result/view/', view_result, name='view_result'),
]