import cf_base_class


class ContestHelper(cf_base_class.CFBaseClass):
    def __init__(self):
        super(ContestHelper, self).__init__()

    def get_contests(self, phase=None):
        contests = self.cf_api.contest_list()['result']
        if not phase:
            return contests
        contests = [contest for contest in contests if contest['phase'] == phase]
        return contests


if __name__ == '__main__':
    ch = ContestHelper()
    ret = ch.get_contests(phase='FINISHED')
    print(len(ret))
