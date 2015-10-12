def has_flag(team, flag):
    for flag_solve in team.solved_flags:
        if flag_solve.flag.flag == flag:
            return True
    return False