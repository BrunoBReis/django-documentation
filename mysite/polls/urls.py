# my imports
from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('specifics/<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('specifics/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('specifics/<int:question_id>/vote/', views.vote, name='vote'),
]
