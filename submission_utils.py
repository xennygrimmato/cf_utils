AC = 'OK'
WRONG_ANSWER = 'WRONG_ANSWER'


def is_ac(submission):
    return submission['verdict'] == AC


def is_wa(submission):
    return submission['verdict'] == WRONG_ANSWER
