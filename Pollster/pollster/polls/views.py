from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Choice, Question
from django.template import loader

# Create your views here.
# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def index(request):
    latest_question_list = Question.objects.order_by('-publication_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
