from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choices

from django.views import generic

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request,pk):
    question = get_object_or_404(Question,pk=pk)
    try:
        selected_choice = question.choices_set.get(pk=request.POST["choice"])
    except (KeyError, Choices.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

