from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('tazelikler/', tazelikler, name='tazelikler'),
    path('habarlasmak/', habarlasmak, name='habarlasmak'),
    path('onumler/', OnumListView.as_view(), name='onumler'),
    path('partnerler/', PartnerListView.as_view(), name='partner_list'),
    path('ammar/', AmmarListView.as_view(), name='ammar'),
    path('sargytlar/', SargytListView.as_view(), name='sargyt_list'),
    path('eksportlar/', EksportListView.as_view(), name='eksport'),
    path('importlar/', importlar_view, name='import'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # path('import/<int:id>/', import_view, name='import_view'),
    # path('import/<int:id>/edit/', import_edit, name='import_edit'),
    # path('import/<int:id>/delete/', import_delete, name='import_delete'),
]