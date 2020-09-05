import concurrent.futures

from codeforces_api import CodeforcesParser

import cf_base_class
import submission_utils


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
        submission_id_to_code = {}
        failed = 0
        succeeded = 0
        for submission in submissions:
            author = self.get_author(submission)
            if author not in author_to_submission:
                author_to_submission[author] = []
            author_to_submission[author].append(submission)

            submission_id_to_code[submission['id']] = ''

        # Get source code for all submissions using ProcessPoolExecutor.
        # The assumption is that there won't be thread-safety issues as all submissions
        # have unique IDs.
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for submission, code in zip(submissions, executor.map(self.get_code, submissions)):
                submission_id_to_code[submission['id']] = code

        for author in author_to_submission:
            try:
                problemwise_mapping = self.get_submissions_of_author_grouped_by_problem(author_to_submission[author],
                                                                                        submission_id_to_code)
                author_to_submission[author] = problemwise_mapping
                succeeded += 1
            except ValueError as ve:
                failed += 1
        print("success: {0}, failure: {1}".format(succeeded, failed))
        return author_to_submission

    def get_code(self, submission):
        try:
            return self.cf_parser.get_solution(contest_id=submission['problem']['contestId'],
                                               submit_id=submission['id'])
        except:
            return ''

    def get_submissions_of_author_grouped_by_problem(self, soafc, submission_id_to_code):
        """Given all submissions made by an author in a contest, group them by problem ID.

        Args:
            - soafc: List of submissions made by an author in a contest

        Returns:
            - Dict[Problem, List[Submission]]: Mapping from problem to all submissions for that problem
        """
        # Add code to submission object
        problem_submission_map = {}
        for submission in soafc:
            prob_id = submission['problem']['index']
            if prob_id not in problem_submission_map:
                problem_submission_map[prob_id] = []
            problem_submission_map[prob_id].append({'submission': submission,
                                                    'code': submission_id_to_code[submission['id']]})
            del submission_id_to_code[submission['id']]
        return problem_submission_map

    def get_incorrect_correct_pairs(self, submissions_by_author_for_problem):
        if len(submissions_by_author_for_problem) < 2:
            return None
        pair = [None, None]  # incorrect, correct
        submission_not_dict_counter = 0
        for submission in submissions_by_author_for_problem:
            if not isinstance(submission, dict):
                submission_not_dict_counter += 1
                continue
            if submission_utils.is_ac(submission):
                pair[1] = submission
            elif submission_utils.is_incorrect(submission):
                pair[0] = submission
        print("Submission objects that are not dict: {0}".format(submission_not_dict_counter))
        return pair

    def get_wa_ac_pairs_for_contest(self, contest_id):
        all_submissions = self.get_submissions(contest_id)['result']
        author_submission_mapping = self.group_submissions_by_author(all_submissions)
        wa_ac_pairs = []
        for author in author_submission_mapping:
            pair = self.get_incorrect_correct_pairs(author_submission_mapping[author])
            if (not pair) or (pair[0] is None) or (pair[1] is None):
                continue
            wa_ac_pairs.append(pair)
        return wa_ac_pairs


if __name__ == '__main__':
    ch = ContestHelper()
    finished_contests = ch.get_contests(phase='FINISHED')
    pairs = ch.get_wa_ac_pairs_for_contest(1409)
    print(pairs)
