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

    # TODO(xennygrimmato): Make method static
    def get_author(self, submission):
        return submission['author']['members'][0]['handle']

    def group_submissions_by_author(self, submissions):
        author_to_submission = {}
        for submission in submissions:
            author = self.get_author(submission)
            if author not in author_to_submission:
                author_to_submission[author] = []
            author_to_submission[author].append(submission)
        return author_to_submission

    def get_code(self, contest_id, submission_id):
        return self.cf_parser.get_solution(contest_id=contest_id, submit_id=submission_id)


if __name__ == '__main__':
    ch = ContestHelper()
    finished_contests = ch.get_contests(phase='FINISHED')
    all_submissions = ch.get_submissions(3)['result']
    author_submission_mapping = ch.group_submissions_by_author(all_submissions)
    code = ch.get_code(3, 90068560)
    print(code)
