from sqlite3 import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from teams.exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)
from teams.models import Team
from django.forms.models import model_to_dict

from teams.utils import data_processing


class TeamView(APIView):
    def post(self, req: Request) -> Response:
        try:
            data_processing(req.data)
            soccer_team_data = req.data

            soccer_team = Team.objects.create(
                name=soccer_team_data["name"],
                titles=soccer_team_data["titles"],
                top_scorer=soccer_team_data["top_scorer"],
                fifa_code=soccer_team_data["fifa_code"],
                first_cup=soccer_team_data["first_cup"],
            )

            soccer_team_dict = model_to_dict(soccer_team)

            return Response(soccer_team_dict, status.HTTP_201_CREATED)

        except NegativeTitlesError as err:
            return Response(
                {"error": f"{err.args[0]}"},
                status.HTTP_400_BAD_REQUEST,
            )
        except InvalidYearCupError as err:
            return Response(
                {"error": f"{err.args[0]}"},
                status.HTTP_400_BAD_REQUEST,
            )
        except ImpossibleTitlesError as err:
            return Response(
                {"error": f"{err.args[0]}"},
                status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as err:
            return Response(
                {
                    "error": "IntegrityError: UNIQUE constraint failed: teams_team.fifa_code"
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, req: Request) -> Response:
        soccer_teams = Team.objects.all()

        teams_list = []

        for team in soccer_teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)


class TeamDetailsView(APIView):
    def get(self, req: Request, team_id: int) -> Response:
        try:
            soccer_team = Team.objects.get(pk=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(soccer_team)
        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, req: Request, team_id: int) -> Response:
        try:
            soccer_team = Team.objects.get(pk=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        req_data_keys = list(req.data.keys())
        req_data_values = list(req.data.values())

        for index, key in enumerate(req_data_keys):
            setattr(soccer_team, key, req_data_values[index])

        soccer_team.save()
        soccer_team_dict = model_to_dict(soccer_team)

        return Response(soccer_team_dict, status.HTTP_200_OK)

    def delete(self, req: Request, team_id: int) -> Response:
        try:
            soccer_team = Team.objects.get(pk=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        soccer_team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
