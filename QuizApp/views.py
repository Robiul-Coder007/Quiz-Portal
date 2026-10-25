from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import *
import random

def register(request):
    if request.user.is_authenticated:
        return redirect('participant')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the Quiz Application.')
            return redirect('participant')
        else:
            messages.error(request, 'Please correct the errors in the registration form.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'page': 'Registration'})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! You have successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/email or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'page': 'Login'})

@login_required(login_url='user_login')
def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password is successfully changed! Please login again.')
            return redirect('user_login')
        else:
            messages.error(request, 'Please correct the error fields below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_pass.html', {'form': form,'page': 'Change Password'})

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully. See you next time!')
    return redirect('user_login')

@login_required(login_url='user_login')
def participant(request):
    if (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Only participants can manage their profile.')
        return redirect('dashboard')
    participant, created = Participant.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, 'Your participant profile has been successfully initialized!')
            else:
                messages.success(request, 'Your profile updates have been successfully saved!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error fields below.')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form, 'page': 'Participant Profile'})

@login_required(login_url='user_login')
def dashboard(request):
    if (request.user.is_staff or request.user.is_superuser):
        quizzes = Quiz.objects.all().order_by('-id')
        quiz_count = quizzes.count()
        context = {
            'page': 'Admin Dashboard',
            'quizzes': quizzes,
            'quiz_count': quiz_count,
            'is_admin': True
        }
        return render(request, 'dashboard.html', context)
    else:
        try:
            participant = request.user.participant
            available_quizzes = Quiz.objects.all().order_by('-id')
            context = {
                'page': 'Participant Dashboard',
                'profile': participant,
                'quizzes': available_quizzes,
                'is_admin': False
            }
            return render(request, 'dashboard.html', context)
        except Participant.DoesNotExist:
            messages.warning(request, 'Please complete your participant profile details first.')
            return redirect('participant')

@login_required(login_url='user_login')
def add_quiz(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Only administrators can manage quizzes.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz has been successfully created!')
            return redirect('dashboard')
    else:
        form = QuizForm()
    return render(request, 'quiz_form.html', {'form': form, 'page': 'Create New Quiz'})

@login_required(login_url='user_login')
def quiz_detail(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    quiz = get_object_or_404(Quiz, id=pk)
    questions = quiz.questions.all().order_by('id')
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions, 'page': f'Quiz: {quiz.title}'})

@login_required(login_url='user_login')
def update_quiz(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    quiz = get_object_or_404(Quiz, id=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz configuration updated successfully!')
            return redirect('quiz_detail', pk=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_form.html', {'form': form, 'page': 'Update Quiz Configuration'})

@login_required(login_url='user_login')
def delete_quiz(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    quiz = get_object_or_404(Quiz, id=pk)
    quiz.delete()
    messages.success(request, 'Quiz has been permanently removed from the system.')
    return redirect('dashboard')

@login_required(login_url='user_login')
def add_question(request, quiz_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Only administrators can manage questions.')
        return redirect('dashboard')
    quiz_obj = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz_obj
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('quiz_detail', pk=quiz_obj.id)
    else:
        form = QuestionForm()
    return render(request, 'quiz_form.html', {'form': form, 'page': f'Add Question to {quiz_obj.title}'})

@login_required(login_url='user_login')
def update_question(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard') 
    question = get_object_or_404(Question, id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question description updated successfully!')
            return redirect('quiz_detail', pk=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'quiz_form.html', {'form': form, 'page': 'Update Question Text'})

@login_required(login_url='user_login')
def delete_question(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    question = get_object_or_404(Question, id=pk)
    quiz_id = question.quiz.id
    question.delete()
    messages.success(request, 'Question removed successfully.')
    return redirect('quiz_detail', pk=quiz_id)

@login_required(login_url='user_login')
def add_option(request, question_id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Only administrators can manage options.')
        return redirect('dashboard')
    question_obj = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question_obj
            option.save()
            messages.success(request, 'Answer option created successfully!')
            return redirect('quiz_detail', pk=question_obj.quiz.id)
    else:
        form = OptionForm()
    return render(request, 'quiz_form.html', {'form': form, 'page': 'Add MCQ Option'})

@login_required(login_url='user_login')
def update_option(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    option = get_object_or_404(Option, id=pk)
    if request.method == 'POST':
        form = OptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            messages.success(request, 'Answer option modified successfully!')
            return redirect('quiz_detail', pk=option.question.quiz.id)
    else:
        form = OptionForm(instance=option)
    return render(request, 'quiz_form.html', {'form': form, 'page': 'Update Answer Option'})

@login_required(login_url='user_login')
def delete_option(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
    option = get_object_or_404(Option, id=pk)
    quiz_id = option.question.quiz.id
    option.delete()
    messages.success(request, 'Answer option deleted.')
    return redirect('quiz_detail', pk=quiz_id)

@login_required(login_url='user_login')
def start_quiz(request, quiz_id):
    if (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Administrators cannot participate in quizzes.')
        return redirect('dashboard')
    try:
        participant = request.user.participant
    except Participant.DoesNotExist:
        messages.warning(request, 'Please complete your participant profile details first before taking a quiz.')
        return redirect('participant')
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # already_taken = QuizResult.objects.filter(participant=participant, quiz=quiz).exists()
    # if already_taken:
    #     messages.warning(request, f"You have already participated in the quiz '{quiz.title}'. Re-taking is not allowed!")
    #     return redirect('dashboard')
    if request.method == 'POST':
        questions = quiz.questions.all()
        total_questions = questions.count()
        correct_count = 0
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    chosen_option = Option.objects.get(id=selected_option_id, question=question)
                    if chosen_option.is_correct:
                        correct_count += 1
                except Option.DoesNotExist:
                    pass
        QuizResult.objects.create(
            participant=participant,
            quiz=quiz,
            score=correct_count,
            total_questions=total_questions,
        )
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0.0
        messages.success(request, f'Quiz submitted successfully! You scored {correct_count} out of {total_questions} ({percentage:.1f}%).')
        return redirect('view_result')
    questions_list = list(quiz.questions.all())
    if not questions_list:
        messages.warning(request, 'This quiz does not have any questions available yet.')
        return redirect('dashboard')
    random.shuffle(questions_list)
    quiz_data = []
    for question in questions_list:
        options = list(question.options.all())
        random.shuffle(options)
        quiz_data.append({
            'question': question,
            'options': options
        })
    context = {
        'page': f'Quiz: {quiz.title}',
        'quiz': quiz,
        'quiz_data': quiz_data,
        'question_count': len(questions_list),
        'profile': participant
    }
    return render(request, 'start_quiz.html', context)

@login_required(login_url='user_login')
def view_result(request):
    if (request.user.is_staff or request.user.is_superuser):
        results = QuizResult.objects.select_related('participant', 'quiz').all().order_by('-score', 'completed_at')
        results_with_positions = []
        for result in results:
            same_quiz_results = QuizResult.objects.filter(quiz=result.quiz).order_by('-score', 'completed_at')
            rank = 1
            for rank_idx, item in enumerate(same_quiz_results, start=1):
                if item.id == result.id:
                    rank = rank_idx
                    break
            results_with_positions.append({
                'result': result,
                'position': rank
            })
        context = {
            'page': 'Global Quiz Results Master Log',
            'results_with_positions': results_with_positions,
            'result_count': len(results_with_positions),
            'is_admin': True
        }
        return render(request, 'view_result.html', context)
    else:
        try:
            participant = request.user.participant
            my_results = QuizResult.objects.select_related('quiz').filter(participant=participant).order_by('-completed_at')
            results_with_positions = []
            for res in my_results:
                same_quiz_results = QuizResult.objects.filter(quiz=res.quiz).order_by('-score', 'completed_at')
                rank = 1
                for rank_idx, item in enumerate(same_quiz_results, start=1):
                    if item.id == res.id:
                        rank = rank_idx
                        break
                results_with_positions.append({
                    'result': res,
                    'position': rank
                })
            context = {
                'page': 'My Quiz Performance Logs',
                'results_with_positions': results_with_positions,
                'result_count': len(results_with_positions),
                'is_admin': False
            }
            return render(request, 'view_result.html', context)
        except Participant.DoesNotExist:
            messages.warning(request, 'Please complete your participant profile details first.')
            return redirect('participant')