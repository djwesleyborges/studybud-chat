from .models import Room

from django.shortcuts import render

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
