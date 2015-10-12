from sqlalchemy.sql import functions, and_

from scoreboard.app import db
from scoring import InjectSolve, Inject


def score_injects(team):
    """
    Calculates the value of all approved injects for a given team

    :param team:  The team to sum
    :return:  The score from injects
    """
    injects = db.session \
        .query(functions.sum(InjectSolve.value_approved)) \
        .filter(and_(InjectSolve.team_id == team.id, InjectSolve.approved == True)) \
        .first()
    injects = injects[0] if injects[0] else 0
    return injects

def team_solve_attempts(team, inject):
    return [solve for solve in team.solved_injects if solve.inject_id == inject.id]

def solve_count(team, inject):
    """
    Counts the number of solves for a given inject by a team

    :param team:  The team to check
    :param inject:   The inject to count
    :return:  The number of solves
    """
    count = 0
    for solve in team.solved_injects:
        if solve.inject_id == inject.id and solve.approved:
            count += 1
    return count


def can_submit_inject(team, inject):
    """
    Checks if a team can submit a solution to a given inject

    :param team:  The team to check
    :param inject:  The inject to check
    :return:  True, if a new solution for the inject can be submitted
    """
    if not inject.can_submit():
        return False
    elif inject.max_solves == Inject.UNLIMITED_SOLVES:
        return True
    else:
        completed = 0
        pending = 0
        for solve in team.solved_injects:
            if solve.inject_id == inject.id:
                if solve.approved is None:
                    pending += 1
                if solve.approved:
                    completed += 1

        return completed + pending < inject.max_solves

def has_pending_solve(team, inject):
    """
    Checks if a team can submit a solution to a given inject

    :param team:  The team to check
    :param inject:  The inject to check
    :return:  True, if a new solution for the inject can be submitted
    """
    for solve in team.solved_injects:
        if solve.inject_id == inject.id:
            if solve.approved is None:
                return True

        return False
