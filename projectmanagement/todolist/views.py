
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from models import Task, TaskStatus
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

# Function which renders user registration page where you can create new users
def registration_page(request):
    context = {}
    user = request.user
    if not str(user) == 'AnonymousUser':
        msg = [{'text': 'Please <a href="/todolist/logout">logout</a> and then visit <a href="/todolist/registration-page">registration page</a> to create user', 'level':'danger', 'code':120, 'persistent':True}]
        context['user_logged_in'] = True
        context['messages'] = msg
        return render(request, 'todolist/register_user.html', context)
    return render(request, 'todolist/register_user.html', context)

# Function which registers new users on the platform
def register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    context = {}

    if User.objects.filter(username=username).exists():
        msg = [{'text': 'This Username is already taken. Please specify a different Username', 'level':'danger', 'code':120, 'persistent':True}]
    else:
        user = User.objects.create_user(username, '', password)
        msg = [{'text': 'Successfully registered the user. Please go to <a href="/todolist">Login page</a> to start creating tasks', 'level':'success', 'persistent':True}]
    
    context['messages'] = msg
    return render(request, 'todolist/register_user.html', context)
    
#Function which helps to authenticate user and log them in
@csrf_exempt
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.filter(username=username)
    auth_user = authenticate(username=username, password=password)
    if auth_user is not None:
        if auth_user.is_active:
            login(request, auth_user)
            # return home(request)
            return HttpResponseRedirect('/todolist')
    else:
        context = {}
        msg = [{'text': 'Please enter valid username and password', 'level':'danger', 'code':120, 'persistent':True}]
        context['messages'] = msg
        return render(request, 'todolist/login.html', context)

# Function which helps to logout the user
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/todolist')

# Function which displays the list of tasks (Completed and Pending tasks)
def index(request):
    user = request.user
    if str(user) == 'AnonymousUser':
        return render(request, 'todolist/login.html')
    context = {}
    user = User.objects.get(username='user1')
    context['tasks'] = Task.objects.all()
    context['all_users'] = User.objects.all()
    return render(request, 'todolist/index.html', context)

# Function which displays individual task details
def task_details(request):
    current_user = request.user
    context = {}
    task_id = request.GET.get('task_id')
    task_obj = Task.objects.get(id=task_id)
    context['task'] = task_obj
    track_list = 'Created by ' + task_obj.created_by.username + ' on ' + task_obj.created_date.strftime('%Y-%m-%d %H:%M')
    for change_status in TaskStatus.objects.filter(task=task_obj).order_by('status_change_date'):
        if change_status.completed:
            track_list += ' --> Closed by ' + change_status.user.username + ' on ' + change_status.status_change_date.strftime('%Y-%m-%d %H:%M')
        else:
            track_list += ' --> Reopened by ' + change_status.user.username + ' on ' + change_status.status_change_date.strftime('%Y-%m-%d %H:%M')

    context['track_list'] = track_list
    print 'track_list = ', track_list
    if task_obj.created_by == current_user:
        context['is_current_user_task'] = True
    else:
        context['is_current_user_task'] = False
    return render(request, 'todolist/task_details.html', context)

# Function which  changes the task staus to completed or pending
def change_task_status(request):
    current_user = request.user
    task_id = request.GET.get('task_id')
    task_obj = Task.objects.get(id=task_id)
    task_status = TaskStatus.objects.create(task=task_obj, user=current_user)
    if task_obj.completed:
        task_obj.completed = False
        task_obj.completed_date = None
        task_status.completed = False
    else:
        task_obj.completed = True
        task_obj.completed_date = now()
        task_status.completed = True
    task_obj.save()
    task_status.save()
    return HttpResponseRedirect('/todolist')

# Function which deletes a task 
def delete_task(request):
    current_user = request.user
    task_id = request.GET.get('task_id')
    task_obj = Task.objects.get(id=task_id)
    if task_obj.created_by == current_user:
        task_obj.delete()
        return HttpResponseRedirect('/todolist')

# Function which saves the edited task 
def edit_task(request):
    current_user = request.user
    task_id = request.POST.get('task_id')
    edited_title = request.POST.get('edited_title')
    edited_description = request.POST.get('edited_description')
    task = Task.objects.get(id=task_id)
    task.title = edited_title
    task.description = edited_description
    task.save()
    return HttpResponseRedirect('/todolist')

# Function which creates new tasks
def create_task(request):
    current_user = request.user
    title = request.POST.get('title')
    description = request.POST.get('description')
    task = Task.objects.create(title=title, description=description, created_by=current_user)
    return HttpResponseRedirect('/todolist')