import json
import os

import erppeek

class OdooProvider(object):
    """
    Odoo API Provider
    """

    def __init__(self, **kwargs):
        """
            project_code: must start with an uppercase letter,
            followed by one or more uppercase alphanumeric characters.
        """
        self._project_name = kwargs.get('project_name', "PROJECT_NAME")
        self._project_key = kwargs.get('project_key', "PROJECT_KEY")
        self._odoo_username = kwargs.get('username')
        self._odoo_password = kwargs.get('password')
        self._odoo_server_url = kwargs.get('api_url')
        self._odoo_database_name = kwargs.get('database_name')
        self._odoo_pm = kwargs.get('pm')

    def setup(self):
        """
            Setup Odoo Project Space
        """
        username = self._odoo_username
        password = self._odoo_password
        odoo_url = self._odoo_server_url
        database = self._odoo_database_name
        pm_id = self._odoo_pm

        odoo_client = erppeek.Client(odoo_url, database, username, password)

        data = {
            'name': self._project_name,
            'project_code': self._project_key,
            'active': True,
            'type': "contract",
            'label_tasks': "Tasks",
            'state': "open",
            'user_id': pm_id,
            'alias_model': "project.task",
            'privacy_visibility': "employees",
            'called_through_ingen_write': True
        }

        project_id = odoo_client.create('project.project', data)
        return project_id
