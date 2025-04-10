from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)
    # Utilizando render no es necesario asignarle valor a una variable template, ni importar loader ni HttpResponse

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

# Atajo 'get_object_or_404' para prácticas dónde haya excepción 404 si no hay objeto 
# from django.shortcuts import get_object_or_404, render
# def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)