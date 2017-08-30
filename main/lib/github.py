import json
import os

from urllib import urlencode
import unirest


class GithubProvider(object):
    """
    Github API Provider
    """

    def __init__(self, **kwargs):
        self._project_name = kwargs.get('project_name', "PROJECT_NAME")
        self._access_token = kwargs.get('access_token')
        self._github_api_url = kwargs.get('api_url')

    def setup(self, callback):
        """
            Setup Github project repository.

            Args:
                callback (function): POST request callback function
        """
        params = {
            'name': self._project_name
        }
        query = {
            'access_token': self._access_token
        }

        unirest.post(
            "{}/user/repos?{}".format(self._github_api_url, urlencode(query)),
            params=json.dumps(params),
            callback=callback
        )
