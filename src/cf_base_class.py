from auth_utils import get_api_key

import codeforces_api


class CFBaseClass:
    def __init__(self):
        key, secret = get_api_key("resources.yml")
        self.cf_api = codeforces_api.CodeforcesApi(key, secret)
