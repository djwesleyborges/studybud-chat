from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import RoomForm
from .models import Room, Topic, Message


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request=request,
                           message='Username or password does not exist.')
    context = {'page': page}
    return render(request=request, template_name='base/login_register.html',
                  context=context)


def logout_page(request):
    logout(request=request)
    return redirect('login')


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
    return render(request=request, template_name='base/login_register.html',
                  context={'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topic = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topic, 'room_count': room_count}
    return render(request=request, template_name='base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request=request, template_name='base/room.html', context=context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!!')

    if request.method == 'POST':
        form = RoomForm(data=request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request=request, template_name='base/delete.html',
                  context={'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request=request, template_name='base/delete.html',
                  context={'obj': message})
