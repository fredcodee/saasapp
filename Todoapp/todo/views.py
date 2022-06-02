from turtle import title
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task
import json

# Create your views here.

#view
def home(request):
  get_tasks = Task.objects.filter(user = request.user).order_by('-id')
  context   = {
    'tasks': get_tasks,
  }
  return render(request, 'home.html', context)



#add
@login_required(login_url='login')
def addTask(request):
  if request.method == 'POST':
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

