from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import*
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import*
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Sum


class OnumListView(ListView):
    model = Onum
    template_name = 'sowda/onumler.html'

class PartnerListView(ListView):
    model = Alyjy
    template_name = 'partner_list.html'

class AmmarListView(ListView):
    model = Ammar
    template_name = 'sowda/ammar.html'


class SargytListView(ListView):
    model = Sargyt
    template_name = 'sargyt_list.html'

class EksportListView(ListView):
    model = EksportSargyt
    template_name = 'sowda/eksport.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EksportSargytForm()
        context['total_kg'] = sum(e.mukdary for e in self.object_list)
        return context

    def post(self, request, *args, **kwargs):
        form = EksportSargytForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eksport')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

def importlar_view(request):
    importlar = ImportHasabat.objects.order_by('-senesi')
    imports = ImportHasabat.objects.all()
    jemi_mukdar = sum([imp.mukdary for imp in imports])
    jemi_baha = sum([imp.baha for imp in imports])
    if request.method == 'POST':
        form = ImportHasabatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('import')
    else:
        form = ImportHasabatForm()

    return render(request, 'sowda/import.html', {
        'form': form,
        'importlar': importlar,
        'jemi_mukdar': jemi_mukdar,
        'jemi_baha': jemi_baha,
    })
# def import_view(request, id):
#     import_obj = get_object_or_404(ImportHasabat, id=id)
#     return render(request, 'sowda/import.html', {'import': import_obj})

# def import_edit(request, id):
#     import_obj = get_object_or_404(ImportHasabat, id=id)
#     return render(request, 'sowda/import.html', {'import': import_obj})

# def import_delete(request, id):
#     import_obj = get_object_or_404(ImportHasabat, id=id)
#     if request.method == "POST":
#         import_obj.delete()
#         return redirect('import')  
#     return render(request, 'sowda/import.html', {'import': import_obj})    
def index(request):
    return render(request, 'sowda/index.html')

def tazelikler(request):
    return render(request, 'sowda/tazelikler.html')

def habarlasmak(request):
    return render(request, 'sowda/habarlasmak.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        if not username or not password:
            messages.error(request, "Maglumatlary doly girizmeli!")
            return redirect('login')

        try:
            
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Ulanyjy adyňyz ýalňyş!")
            return redirect('login')  
        user = authenticate(request, username=user.username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            next_url = request.GET.get('next', 'index')  
            return redirect(next_url)  
        
        messages.error(request, "Ulanyjy hasaby ýok!")
        return redirect('login')  

    return render(request, 'sowda/login.html')  


def logoutView(request):
    logout(request)
    return redirect('login')


def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        confirm_password = request.POST.get('confirm_password')  
        if not email or not password or not username:
            messages.error(request, _("Maglumatlary doly girizmeli"))
            return redirect('register')

        if password != confirm_password:
            messages.error(request, _("Parollar bir-birine deň bolmaly"))
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, _("Bu e-mail salgy üçin hasap döredilen"))
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, _("Bu ulanyjy ady üçin hasap döredilen"))
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, _("Hasap döredildi"))
        return redirect('login')  

    return render(request, 'sowda/login.html')

def dashboard_view(request):
    years = ["2021", "2022", "2023", "2024"]
    eksport_data = []
    import_data = []

    for y in years:
        eksport_total = EksportSargyt.objects.filter(senesi__year=y).aggregate(total=Sum('mukdary'))['total'] or 0
        import_total = ImportHasabat.objects.filter(senesi__year=y).aggregate(total=Sum('mukdary'))['total'] or 0
        eksport_data.append(eksport_total)
        import_data.append(import_total)

    monthly_data = []
    monthly_labels = ['Ýan', 'Few', 'Mar', 'Apr', 'Maý', 'Iýn', 'Iýl', 'Awg', 'Sen', 'Okt', 'Noý', 'Dek']
    for m in range(1, 13):
        total = EksportSargyt.objects.filter(senesi__year=2024, senesi__month=m).aggregate(total=Sum('mukdary'))['total'] or 0
        monthly_data.append(total)

    country_qs = EksportSargyt.objects.values('partner').annotate(total=Sum('mukdary')).order_by('-total')[:5]
    top_countries_labels = [c['partner'] for c in country_qs]
    top_countries_data = [c['total'] for c in country_qs]

    return render(request, 'sowda/dashboard.html', {
        'years': years,
        'eksport_data': eksport_data,
        'import_data': import_data,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
        'top_countries_labels': top_countries_labels,
        'top_countries_data': top_countries_data
    })