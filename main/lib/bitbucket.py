import os
import unirest

def get_bitbucket_git_url(owner, project_name):
    """
        Returns the git url of the created repository from bitbucket
    """
    return "ssh://git@bitbucket.org/{}/{}.git".format(owner, project_name)


class BitbucketProvider(object):
    """
    Bitbucket API Provider
    """

    def __init__(self, **kwargs):
        self._project_name = kwargs.get('project_name', "PROJECT_NAME").replace(" ", "-").lower()
        self._bitbucket_username = kwargs.get('username')
        self._bitbucket_password = kwargs.get('password')
        self._bitbucket_api_url = kwargs.get('api_url')

    def setup(self, callback):
        """
            Setup Bitbucket project repository.

            Args:
                callback (function): POST request callback function
        """

        # configure the project repository
        data = {
            'name': self._project_name,
            'is_private': True
        }
        unirest.post(
            url = "{}/repositories".format(self._bitbucket_api_url),
            auth=(self._bitbucket_username, self._bitbucket_password),
            params=data,
            callback=callback
        )
