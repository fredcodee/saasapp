from http import server
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Task
import json
from memberships.views import get_user_subscription, getuser_membership

# Create your views here.

#view

#free membership only 3 task
#others unlimited


def home(request):
  if request.user.is_authenticated:
    get_tasks = Task.objects.filter(user = request.user).order_by('-id')
  else:
    get_tasks = {'register/login to modify your tasks'}
  context   = {
    'tasks': get_tasks,
  }
  return render(request, 'home.html', context)



#add
@login_required(login_url='login')
def addTask(request):
  if request.method == 'POST':
    #check users membership plan
    userSub = get_user_subscription(request) 
    usermem = getuser_membership(request)

    try:
      if  usermem.membership.membership_type == 'Free' or  not userSub.active:
        if len(Task.objects.filter(user = request.user))> 2:
          messages.error(request, 'you have already exhuasted your free tasks, subscribed to any plan to get unlimited tasks')
          return redirect('home')
    except:
      if len(Task.objects.filter(user = request.user))> 2:
          messages.error(request, 'you have already exhuasted your free tasks, subscribed to any plan to get unlimited tasks')
          return redirect('home')

    title = request.POST['title']
    new_task = Task(title = title, user = request.user, completed = False)
    new_task.save()

  return redirect('home')


  

#check
@login_required(login_url='login')
def checkTask(request):
  data = json.loads(request.body)
  taskId = data['taskId']
  action  = data['action']

  get_task = Task.objects.get(id = taskId)
  if action == 'False':
    get_task.completed = True
  else:
    get_task.completed = False
  
  get_task.save()


  return JsonResponse('marked as done', safe = False)



#delete
@login_required(login_url='login')
def DeleteTask(request):
  data = json.loads(request.body)
  taskId = data['taskId']

  get_task = Task.objects.get(id = taskId)
  get_task.delete()

  return JsonResponse('deleted', safe = False)


#errors
def handle_not_found(request, exception):
  return render(request, 'errors_page/not-found.html')


def handle_server_error(request):
  return render(request, 'errors_page/server-error.html')


#hosting