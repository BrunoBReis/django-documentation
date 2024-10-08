from django.shortcuts import get_object_or_404, render
# my imports
from django.db.models import F
# using render instead of HttpResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question

# Create your views here.

###### WITHOUT USING RENDER ######
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

###### NOT GENERT VIEW ######
# def index(request):
#     # up to five questions
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

###### WITHOUT USING RENDER ######
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})

###### NOT A GENERIC VIEW ######
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

###### NOT A GENERIC VIEW ######
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

###### SIMPLE VOTE TAMPLATE ######
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)


class DetailView(generic.DetailView):
    """ Generic view for detail page """
    model = Question
    template_name = "polls/detail.html"


class IndexView(generic.ListView):
    """ Generic view for index page """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions """
        return Question.objects.order_by("-pub_date")[:5]


class ResultsView(generic.DetailView):
    """ Generic view for results page """
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """ Vote on a question """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {
            "question": question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
