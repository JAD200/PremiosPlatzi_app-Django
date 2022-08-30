from django.urls import path

from . import views

urlpatterns = [
    # * ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/detail/5
    path("detail/<int:question_id>", views.detail, name="detail"),
    # ex: /polls/results/5
    path("results/<int:question_id>", views.results, name="results"),
    # ex: /polls/vote/5
    path("vote/<int:question_id>", views.vote, name="vote"),
]
