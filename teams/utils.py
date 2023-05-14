from datetime import datetime, timedelta
from logging import exception
from teams.exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


def check_world_cup_year(world_cup_year: int) -> bool:
    first_cup = 1930

    num_of_years_since_first_worls_cup = world_cup_year - first_cup
    if (num_of_years_since_first_worls_cup >= 0) and (
        num_of_years_since_first_worls_cup % 4 == 0
    ):
        return True

    return False


def check_possible_number_of_titles(titles: int, first_cup: int) -> bool:
    current_date = datetime.now()
    current_year = int(current_date.year)

    total_world_cups = (current_year - first_cup) / 4
    if titles >= total_world_cups:
        return True

    return False


def data_processing(national_soccer_team: dict) -> None:
    if national_soccer_team["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    first_world_cup_year = int(national_soccer_team["first_cup"][:4])
    if not (check_world_cup_year(first_world_cup_year)):
        raise InvalidYearCupError("there was no world cup this year")

    if check_possible_number_of_titles(
        national_soccer_team["titles"], first_world_cup_year
    ):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
