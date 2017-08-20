from django.shortcuts import render
from django.views.generic.base import TemplateView


class SofaView(TemplateView):
    template_name = 'sofa/index.html'
