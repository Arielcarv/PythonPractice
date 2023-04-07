from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question


# Create your views here.


# Get all questions and display them.
def index(request):
    latest_question_list = Question.objects.order_by("-publication_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


# Show specific question and choices.
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, "polls/details.html", {"question": question})


# Get question and display results.
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


# Vote on a specific question.
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice.get(pk=request.POST["choice"])
    except (KeyError, Choice.doesNotExist):
        # Re-render the voting form cause the one you wanted doesn't exist.
        context = {
            "question": question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/details.html", context)
    selected_choice.votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after success on sending POST request data.
    # This prevents data form being posted twice if user hits the BACK BUTTON.
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
