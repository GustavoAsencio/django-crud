from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from django.contrib import messages
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'home.html')
    
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html',{'form':UserCreationForm})
    else:
        
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except:
                return render(request,'signup.html',{'form':UserCreationForm,'error':'El usuario ya existe'})
        return render(request,'signup.html',{'form':UserCreationForm,'error':'Las contraseñas no coinciden'})
    
@login_required
def task(request):
    tasks = Task.objects.filter(user=request.user,dateCompleted__isnull=True ).order_by('-created')
    return render(request, 'task.html', {'tasks':tasks})
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    data = {'form':AuthenticationForm()}
    if request.method == 'GET':
        return render(request, 'signin.html', data)    
    else:
        user = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=user, password=password)
        if user is not None:
            login(request, user)
            return redirect('task')
            
        else:
            data = {'form':AuthenticationForm,'error':'Los datos son incorrectos'}
            return render(request, 'signin.html', data)
    
@login_required
def createTask(request):
    if request.method == 'GET':        
        data = {'form': TaskForm}
        return render(request, 'create_task.html', data)
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            
            messages.success(request, 'La tarea se ha creado con éxito.')
            return redirect('task')
        else:
            data = {'form': form}
            messages.error(request, 'Se ha producido un error al procesar la solicitud.')
            return render(request, 'create_task.html', data)

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':        
        id = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=id)
        data = {'task': id, 'form': form}
        return render(request, 'task_detail.html', data)
    else:
        try:
            id = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST  , instance=id)
            form.save()
            return redirect('task')
        except ValueError:
            messages.error(request, 'Se ha producido un error al procesar la solicitud.')
            return render(request, 'task_detail.html', 
                          {'task_id': id, 
                           'form': form, 
                           'error':'Se ha producido un error al procesar la solicitud.'})


@login_required   
def deleteTask(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        messages.success(request, 'La tarea se ha eliminado con éxito.')
        return redirect('task')

@login_required
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':   
        task.dateCompleted = timezone.now()
        task.save()
        messages.success(request, 'La tarea se ha completado con éxito.')
        return redirect('task')
@login_required
def completedTasks(request):
    tasks = Task.objects.filter(user=request.user,dateCompleted__isnull=False ).order_by('-dateCompleted')
    return render(request, 'completed_tasks.html', {'tasks':tasks})