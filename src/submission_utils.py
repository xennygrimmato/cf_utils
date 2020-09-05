AC = 'OK'
WRONG_ANSWER = 'WRONG_ANSWER'
TLE = 'TIME_LIMIT_EXCEEDED'
MLE = 'MEMORY_LIMIT_EXCEEDED'
COMPILATION_ERROR = 'COMPILATION_ERROR'


def is_ac(submission):
    return submission['verdict'] == AC


def is_wa(submission):
    return submission['verdict'] == WRONG_ANSWER


def is_tle(submission):
    return submission['verdict'] == TLE


def is_mle(submission):
    return submission['verdict'] == MLE


def is_ce(submission):
    return submission['verdict'] == COMPILATION_ERROR


def is_incorrect(submission):
    return is_wa(submission) or is_tle(submission) or is_mle(submission) or is_ce(submission)
