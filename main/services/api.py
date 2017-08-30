
from django.http import HttpResponse
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response

from lib.jumpstart import Jumpstart

from core.utils import send_email_template
from .models import (
    Service,
    Template,
    Setting,
)
from .serializers import ServiceSerializer


class JumpStartAPIView(APIView):

    def post(self, request, *args, **kwargs):
        project_name = request.data.get('project_name')
        project_key = request.data.get('project_key')
        repo = request.data.get('repo', "")
        pm_tool = request.data.get('pm_tool', "")
        template_type = request.data.get('template_type', 0)
        
        repo_service = Service.objects.filter(identifier__in=[repo, pm_tool])
        repo_serializer = ServiceSerializer(repo_service, many=True).data
        
        service_data = {}
        
        for rr in repo_serializer:
            rs_settings = rr.get('settings')
            service_data[rr.get('service_type')] = {}
            for r in rs_settings:
                service_data[rr.get('service_type')][r.get('identifier')] = r.get('value')
            
        template = Template.objects.get(template_type=template_type)
        
        js = Jumpstart(**{
            'project_name': project_name,
            'project_key': project_key,
            'repository': repo,
            'pm_tool': pm_tool,
            'template_url': template.repo_url,
            'service_data': service_data
        })
        
        email_subj = "{} PROJECT SUCCESSFULY CREATED".format(project_name)
        
        email_body = "Project Successfuly Created\n" \
                    "Repository URL: {}\nPM Tool URL: {}".format(js.get_repo_url(), js.get_pm_tool_url())
        
        send_email_template(email_subj, "", [request.user.email], email_body)

        return Response({
            'pm_tool_url': js.get_pm_tool_url(),
            'repo_url': js.get_repo_url()
            })
