from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import F
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Choice, Question

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
# def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # Hace explícito que solo un POST modifique los datos (choice)
    except (KeyError, Choice.DoesNotExist):
        # Si no recibe choice, levanta una excepción y muestra el formulario con la misma pregunta
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Si recibe choice, incrementa los votos en 1, lo guarda y redirige al usuario a la página de resultados
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        # HttpResponseRedirect es una buena práctica (distinto a HttpResponse). Evita que si el usuario actualiza la página el formulario se vuelva a enviar
        # La función reverse() ahorrar la codificación de una URL