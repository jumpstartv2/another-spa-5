import json
import os

import unirest


class JiraProvider(object):
    """
    Jira API Provider
    """

    def __init__(self, **kwargs):
        """
            project_key: must start with an uppercase letter,
            followed by one or more uppercase alphanumeric characters.
        """
        self._project_name = kwargs.get('project_name', "PROJECT_NAME")
        self._project_key = kwargs.get('project_key', "PROJECT_KEY")
        self._jira_username = kwargs.get('username')
        self._jira_password = kwargs.get('password')
        self._jira_api_url = kwargs.get('api_url')

    def setup(self, callback):
        """
            Setup Jira Project Space

            Args:
                callback (function): POST request callback function
        """
        data = {
            'key': self._project_key.upper(),
            'name': self._project_name,
            'projectTypeKey': "software",
            'lead': "admin",
        }

        unirest.post(
            url = "{}/rest/api/2/project/".format(self._jira_api_url),
            auth=(self._jira_username, self._jira_password),
            headers={'Content-Type': "application/json" },
            params=json.dumps(data),
            callback=callback
        )

