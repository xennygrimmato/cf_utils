import cf_base_class

from codeforces_api import CodeforcesParser


class ContestHelper(cf_base_class.CFBaseClass):
    def __init__(self):
        super(ContestHelper, self).__init__()
        self.cf_parser = CodeforcesParser()

    def get_contests(self, phase=None):
        contests = self.cf_api.contest_list()['result']
        if not phase:
            return contests
        contests = [contest for contest in contests if contest['phase'] == phase]
        return contests

    def get_submissions(self, contest_id):
        status = self.cf_api.contest_status(contest_id=contest_id)
        return status

    def get_author(self, submission):
        return submission['author']['members'][0]['handle']

    def group_submissions_by_author(self, submissions):
        author_to_submission = {}
        failed = 0
        succeeded = 0
        for submission in submissions[:100]:
            author = self.get_author(submission)
            if author not in author_to_submission:
                author_to_submission[author] = []
            author_to_submission[author].append(submission)
        for author in author_to_submission:
            try:
                problemwise_mapping = self.get_submissions_of_author_grouped_by_problem(author_to_submission[author])
                author_to_submission[author] = problemwise_mapping
                succeeded += 1
            except ValueError as ve:
                failed += 1
        print("success: {0}, failure: {1}".format(succeeded, failed))
        return author_to_submission

    def get_code(self, contest_id, submission_id):
        return self.cf_parser.get_solution(contest_id=contest_id, submit_id=submission_id)

    def get_submissions_of_author_grouped_by_problem(self, soafc):
        """Given all submissions made by an author in a contest, group them by problem ID.

        Args:
            - soafc: List of submissions made by an author in a contest

        Returns:
            - Dict[Problem, List[Submission]]: Mapping from problem to all submissions for that problem
        """
        problem_submission_map = {}
        for submission in soafc:
            sub_id = submission['id']
            prob_id = submission['problem']['index']
            code = self.get_code(submission['problem']['contestId'], sub_id)
            if prob_id not in problem_submission_map:
                problem_submission_map[prob_id] = []
            problem_submission_map[prob_id].append({'submission': submission,
                                                    'code': code})
        return problem_submission_map


if __name__ == '__main__':
    ch = ContestHelper()
    finished_contests = ch.get_contests(phase='FINISHED')
    all_submissions = ch.get_submissions(1409)['result']
    author_submission_mapping = ch.group_submissions_by_author(all_submissions)
    print(author_submission_mapping)
