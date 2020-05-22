from typing import Any, Tuple, Callable, Set
from sys import argv

import codeforces_api
import yaml


def get_api_key(path: str) -> Tuple[str, str]:
    with open(path, 'r') as stream:
        try:
            d = yaml.safe_load(stream)
            return d['key'], d['secret']
        except yaml.YAMLError as exc:
            print(exc)


class SpecialProblems:
    def __init__(self):
        key, secret = get_api_key("resources.yml")
        self.cf_api = codeforces_api.CodeforcesApi(key, secret)
        self.problem_to_tags_map = {}

    def get_problem_link(self, submission):
        return "https://codeforces.com/contest/{contestId}/problem/{index}".format(contestId=submission['contestId'],
                                                                                   index=submission['problem']['index'])

    async def get_problems_by_handle(self, handle: str, filter_fn: Callable) -> Set[Any]:
        submissions = self.cf_api.user_status(handle=handle).get('result')
        return set([(submission['problem']['name'], self.get_problem_link(submission)) for submission in submissions
                    if submission['verdict'] == 'OK' and filter_fn(submission)])


def print_problems(problems, path, fmt='txt'):
    if len(problems) == 0:
        print("No problems found!")
    with open(path, 'w') as f:
        for problem in problems:
            f.write("{problem_name}: {problem_link}\n".format(problem_name=problem[0], problem_link=problem[1]))
        print("Finished writing {0} problems to file {1}".format(len(problems), path))


if __name__ == '__main__':
    min_problem_rating = int(argv[1])
    handles = argv[2:]
    api = SpecialProblems()
    problem_sets_per_handle = {
        handle: api.get_problems_by_handle(handle,
                                           lambda submission: 'rating' in submission['problem'] and
                                                              submission['problem']['rating'] >= min_problem_rating)
        for handle in handles
    }
    common_problems = set.intersection(*(problem_sets_per_handle[handle] for handle in handles))
    print_problems(common_problems, str(min_problem_rating) + '_' + '_'.join(handles) + '.txt')
