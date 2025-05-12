from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView


# Create your views here.
class RulestView(TemplateView):
    template_name = 'main/rules.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Car - Shop'
        context['content'] = "Car Shop Center"
        return context

    def get(self, request, *args, **kwargs):
        # Matnni JSON formatda yuborish
        return JsonResponse({
            'title': 'Car - Shop',
            'content': 'Car Shop Center'
        })