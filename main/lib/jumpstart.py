import os
import json
from os.path import (
    dirname,
    join
)

from lib.bitbucket import BitbucketProvider, get_bitbucket_git_url
from lib.github import GithubProvider
from lib.jira import JiraProvider
from lib.odoo import OdooProvider


class Jumpstart(object):

    def __init__(self, *args, **kwargs):
        self.PROJECT_NAME = kwargs.get('project_name', "PROJECT_NAME").replace(" ", "-").lower()
        self.PROJECT_KEY = kwargs.get('project_key', "PROJECT_KEY")
        self.PROJECT_DIR = os.path.join('build', "jumpstart", self.PROJECT_NAME)
        self.REPOSITORY = int(kwargs.get('repository', ""))
        self.PM_TOOL = int(kwargs.get('pm_tool', ""))
        self.REPO_URL = ""
        self.PM_TOOL_URL = ""
        self.TEMPLATE_URL = kwargs.get('template_url', "")
        self.SERVICE_DATA = kwargs.get('service_data', {})
        self.process(**kwargs)

    def _clone_web_repo_url(self):
        """
            Function that will clone the chosen web framework(Django or Django REST)
            in the created project_dir in build/.

            Args:
                id (int): ID of the Django Templates (DJANGO_TEMPLATES_REPOS, DJANGO_REST_TEMPLATES_REPOS)
                type (int): Value that will determine if the user chose DJANGO or DJANGO REST
        """
        print "cloning..."
        os.system("git clone {} {}".format(self.TEMPLATE_URL, self.PROJECT_DIR))

    def _create_build_directory(self):
        """
            Function that will create project directory based on `Project Name` given by the user
            or the default.
        """
        print "build directory..."
        os.system("mkdir -p build/jumpstart/{}".format(self.PROJECT_NAME))

    def _push_to_repo(self, project_name, repo_url):
        """
            Function that will push Jumpstart Project Build to respective
            repository.

            Args:
                project_name: The Project Name provided by the user
                repo_url: The `HTTPS` Repository url
        """
        print "pushing..."
        os.system("cd build/jumpstart/{} && git remote set-url origin {} && git push -u origin master".format(
            project_name,
            repo_url))

    def _create_github_repo_callback(self, response):
        """
            Function that will return Github API's response and integrate the
            _push_to_repo function.
        """
        if response.code == 201:
            print 'success: _create_github_repo_callback'
            self.REPO_URL = response.body.get('ssh_url')
            self._push_to_repo(self.PROJECT_NAME, self.REPO_URL)
        else:
            #handle error
            pass

    def _create_bitbucket_repo_callback(self, response):
        """
            Function that will return Bitbucket API's response and integrate the
            _push_to_repo function.
        """
        if response.code == 200:
            print 'success: _create_bitbucket_repo_callback'
            bitbucket_url =  get_bitbucket_git_url(
                response.body.get('owner'),
                response.body.get('name')
            )
            self.REPO_URL = bitbucket_url
            self._push_to_repo(self.PROJECT_NAME, self.REPO_URL)
        else:
            #handle error
            pass

    def _create_jira_project_callback(self, response):
        """
            Function that will return Jira API's response.
        """
        body = json.loads(response.raw_body)
        
        if body.get('self'):
            self.PM_TOOL_URL = body.get('self')
            print 'success: _create_jira_project_callback'
            print self.PM_TOOL_URL
        else:
            print 'error: _create_jira_project_callback'

    def _create_odoo_project_callback(self, response):
        if isinstance(response, int):
            pass
            #handle success
        else:
            pass
            #handle error

    def _create_github_repo(self):
        """
            Function that will create Github repository
        """
        
        serv_data = self.SERVICE_DATA.get('repository')
        github = GithubProvider(**{
            'project_name': self.PROJECT_NAME,
            'access_token': serv_data.get('access_token'),
            'api_url': serv_data.get('api_url'),
        })
        github.setup(self._create_github_repo_callback)

    def _create_bitbucket_repo(self):
        """
            Function that will create Bitbucket repository
        """
        serv_data = self.SERVICE_DATA.get('repository')
        bitbucket = BitbucketProvider(**{
            'project_name': self.PROJECT_NAME,
            'username': serv_data.get('username'),
            'password': serv_data.get('password'),
            'api_url': serv_data.get('api_url'),
        })
        bitbucket.setup(self._create_bitbucket_repo_callback)

    def _create_jira_project(self):
        """
            Function that will create Jira project
        """
        serv_data = self.SERVICE_DATA.get('pm_tool')
        
        jira = JiraProvider(**{
            'project_name': self.PROJECT_NAME,
            'project_key': self.PROJECT_KEY,
            'api_url': serv_data.get('api_url'),
            'username': serv_data.get('username'),
            'password': serv_data.get('password'),
        })
        jira.setup(self._create_jira_project_callback)

    def _create_odoo_project(self):
        serv_data = self.SERVICE_DATA.get('pm_tool')
        
        odoo = OdooProvider(**{
            'project_name': self.PROJECT_NAME,
            'project_key': self.PROJECT_KEY,
            'api_url': serv_data.get('api_url'),
            'username': serv_data.get('username'),
            'password': serv_data.get('password'),
            'database_name': serv_data.get('database_name'),
            'pm': serv_data.get('pm'),
        })
        resp = odoo.setup()
        self._create_odoo_project_callback(resp)
        
    def get_pm_tool_url(self):
        return self.PM_TOOL_URL
        
    def get_repo_url(self):
        return self.REPO_URL

    def process(self, **kwargs):
        """
            Function that will integrate all functions

            Args:
                kwargs (dict): A dictionary of all required/needed data from user.
                0 - github
                1- bitbucket
                2 - jira
                3 - odoo
        """

        if self.REPOSITORY != "":
            if self.REPOSITORY == 0:
                self._create_github_repo()
            else:
                self._create_bitbucket_repo()
                
        if self.PM_TOOL != "":
            if self.PM_TOOL == 2:
                self._create_jira_project()
            else:
                self._create_odoo_project()
                
        self._create_build_directory()
        self._clone_web_repo_url()
