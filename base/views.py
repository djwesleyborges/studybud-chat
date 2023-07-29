from .models import Room
from .forms import RoomForm
from django.shortcuts import render, redirect

rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn Vue!'},
    {'id': 3, 'name': 'Lets learn Flask!'},
]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
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
        room.save()
        return redirect('home')
    return render(request=request, template_name='base/delete.html', context={'obj': room})