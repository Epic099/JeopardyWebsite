from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lobby, Player
import string
import random

def getRandomId(length : int):
    digits = string.digits

    return "".join(random.sample(digits, length))
# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@login_required(login_url="/login")
def join(request):
    return render(request, 'lobby/join.html')

@login_required(login_url="/login")
def create(request):
    
    id = getRandomId(8)
    
    l = Lobby.objects.create(Lobby_id=id, host = request.user)
    
    l.save()
    
    return redirect(f"/lobby/{id}")

@login_required(login_url="/login")
def lobby(request, id):     
    lob = None
    try:
        lob = Lobby.objects.get(Lobby_id=id)
    except Exception as error:
        user = request.user
        print(f"{user.username} tried to join Lobby {id}. Error: Lobby does not exist. Redirecting back...")
    if lob is None:
        return redirect("/join")
    user = request.user
    host = 0
    if lob.host != user:
        p = Player.objects.filter(user=user).first()
        if p is not None:
            p.delete()
        
        p = Player.objects.create(user=user, name=user.username)
        p.save()
        lob.users.add(p)
    else:
        host = 1
    b = lob.get_board()
    c1,c2,c3,c4,c5 = b.categories[0].name, b.categories[1].name, b.categories[2].name, b.categories[3].name, b.categories[4].name
    players = lob.users.all()
    return render(request, 'lobby/lobby.html', context={"lobby_id" : id, "host" : host, "players" : players, "c1" : c1, "c2" : c2, "c3" : c3, "c4" : c4, "c5" : c5})