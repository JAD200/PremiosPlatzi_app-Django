from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Estas en la pagina principal de <h1>Premios Platzi App</h1>')


def detail(request, question_id):
    return HttpResponse(f'Estas viendo la pregunta numero {question_id}')


def results(request, question_id):
    return HttpResponse(f'Estas viendo los resultados de la pregunta numero {question_id}')


def vote(request, question_id):
    return HttpResponse(f'Estas votando a la pregunta numero {question_id}')
