from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.shortcuts import render, redirect

rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn Vue!'},
    {'id': 3, 'name': 'Lets learn Flask!'},
]


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
    rooms = Room.objects.get(id=pk)
    context = {'room': rooms}
    return render(request=request, template_name='base/room.html', context=context)


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(data=request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request=request, template_name='base/delete.html',
                  context={'obj': room})
