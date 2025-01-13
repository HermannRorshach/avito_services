from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import DeleteView, DetailView, ListView

from django.views import View


@method_decorator(login_required, name='dispatch')
class CabinetView(View):
    template_name = 'accounts/cabinet.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Create your views here.
class ServicesView(View):
    template_name = 'accounts/services.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ContactsView(TemplateView):
    template_name = 'accounts/contacts.html'


class FAQView(TemplateView):
    template_name = 'accounts/faq.html'
