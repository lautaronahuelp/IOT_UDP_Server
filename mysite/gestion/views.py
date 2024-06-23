from django.shortcuts import render
from .models import Comando

# Create your views here.
def lista_comandos(request):
    comandos = Comando.objects.all()
    return render(request, 'gestion/lista_comandos.html', { 'comandos': comandos, })