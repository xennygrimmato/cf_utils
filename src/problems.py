from typing import Any, Tuple, Callable, Set, List, Union
from sys import argv

import codeforces_api

from cf_base_class import CFBaseClass


class SpecialProblems(CFBaseClass):
    def __init__(self):
        super(SpecialProblems, self).__init__()
        self.problem_to_tags_map = {}

    def get_problem_link(self, submission):
        return "https://codeforces.com/contest/{contestId}/problem/{index}".format(contestId=submission['contestId'],
                                                                                   index=submission['problem']['index'])

    def get_problems_by_handle(self, handle: str) -> Set[Any]:
        submissions = self.cf_api.user_status(handle=handle).get('result')
        return submissions

    def get_problem_ratings(self, submissions):
        return [submission['problem']['rating'] for submission in submissions]

    def get_ac_submissions(self, handle, filter_fn: Callable):
        submissions = self.get_problems_by_handle(handle)
        return set([(submission['problem']['name'], self.get_problem_link(submission), submission['problem']['rating'])
                    for submission in submissions
                    if submission['verdict'] == 'OK' and filter_fn(submission)])


def print_problems(problems, path, fmt='txt'):
    if len(problems) == 0:
        print("No problems found!")
    with open(path, 'w') as f:
        problems.sort(key=lambda x: x[2])
        for problem in problems:
            f.write("{problem_name}: {problem_link} | {problem_rating}\n".format(problem_name=problem[0],
                                                                                 problem_link=problem[1],
                                                                                 problem_rating=problem[2]))
        print("Finished writing {0} problems to file {1}".format(len(problems), path))


if __name__ == '__main__':
    min_problem_rating = int(argv[1])
    handles = argv[2:]
    api = SpecialProblems()
    problem_sets_per_handle = {
        handle: api.get_ac_submissions(handle,
                                           lambda submission: 'rating' in submission['problem'] and
                                                              submission['problem']['rating'] >= min_problem_rating)
        for handle in handles
    }
    common_problems = set.intersection(*(problem_sets_per_handle[handle] for handle in handles))
    print_problems(list(common_problems), str(min_problem_rating) + '_' + '_'.join(handles) + '.txt')
