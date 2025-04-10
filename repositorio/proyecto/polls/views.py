from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Opción 1: usar ListView y la función get_queryset(self)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    # Por defecto, se enviaría al template una variable question_list
    context_object_name = "latest_question_list"
    # Con context_object_name, lo puedo personalizar

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    # Retorna las últimas 5 encuestas

# Opción 2: usar DetailView y setear el valor de model
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Siempre se utiliza template_name para usar una plantilla específica

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