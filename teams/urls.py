from django.urls import path
from teams.views import TeamDetailsView, TeamView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamDetailsView.as_view()),
]
