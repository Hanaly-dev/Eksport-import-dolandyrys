from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import*
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages

class OnumListView(ListView):
    model = Onum
    template_name = "onum_list.html"

class AmmarListView(ListView):
    model = Ammar
    template_name = "ammar_list.html"

class EksportSargytCreateView(CreateView):
    model = EksportSargyt
    fields = ['onum', 'mukdary', 'partner']
    template_name = "eksport_sargyt_form.html"
    success_url = reverse_lazy("eksport-list")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

class ImportHasabatCreateView(CreateView):
    model = ImportHasabat
    fields = ['onum', 'mukdary', 'ýurt']
    template_name = "import_form.html"
    success_url = reverse_lazy("import-list")

class PartnerListView(ListView):
    model = Partner
    template_name = "partner_list.html"

class SargytListView(ListView):
    model = Sargyt
    template_name = "sargyt_list.html"
def index(request):
    return render(request, 'sowda/index.html')

def tazelikler(request):
    return render(request, 'sowda/tazelikler.html')

def habarlasmak(request):
    return render(request, 'sowda/habarlasmak.html')
