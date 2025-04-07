from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('tazelikler/', tazelikler, name='tazelikler'),
    path('habarlasmak/', habarlasmak, name='habarlasmak'),
    path('onumler/', OnumListView.as_view(), name='onum-list'),
    path('ammar/', AmmarListView.as_view(), name='ammar-list'),
    path('eksport-gos/', EksportSargytCreateView.as_view(), name='eksport-gos'),
    path('import-gos/', ImportHasabatCreateView.as_view(), name='import-gos'),
    path('partnerler/', PartnerListView.as_view(), name='partner-list'),
    path('sargytlar/', SargytListView.as_view(), name='sargyt-list'),
]